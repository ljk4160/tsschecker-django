import os
import time
import json
import django_rq
import subprocess

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from multiprocessing import TimeoutError
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext as _


from MetaManagement.models import Device, Signature
from django_rq import queues


def handle_signing_task(request_dict, throw_exception):

    def tsschecker(ecid, product_type, hw_model, ios_version, ios_build, ap_nonce, is_ota):
        cmd = 'tsschecker'
        cmd = cmd + ' -e ' + ecid
        cmd = cmd + ' -d ' + product_type
        cmd = cmd + ' -i ' + ios_version
        if len(hw_model) > 0:
            cmd = cmd + ' -B '+ hw_model
        if len(ios_build) > 0:
            cmd = cmd + ' --buildid ' + ios_build
        if len(ap_nonce) > 0:
            cmd = cmd + ' --apnonce ' + ap_nonce
        if is_ota:
            cmd = cmd + ' -o'
        cmd = cmd + ' -s'
        save_prefix = 'resources/'
        save_path = 'shsh2/' + ecid + '/'
        try:
            os.mkdir(save_prefix + save_path, 0755)
        except:
            pass
        if len(ios_build) > 0:
            save_path = save_path + ios_version + '-' + ios_build + '/'
        else:
            save_path = save_path + ios_version + '/'
        try:
            os.mkdir(save_prefix + save_path, 0755)
        except:
            pass
        cmd = cmd + ' --save-path ' + save_prefix + save_path
        print('[Execute] ' + cmd)
        timeout = 30
        res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (sout, serr) = res.communicate()
        t_beginning = time.time()
        while True:
            if res.poll() is not None:
                break
            seconds_passed = time.time() - t_beginning
            if timeout and seconds_passed > timeout:
                res.terminate()
                raise TimeoutError(cmd, timeout)
            time.sleep(0.1)
        return res.returncode, sout, serr, res.pid, save_path

    result_dict = {}

    required_fields = ['ecid', 'ios_version']
    for field in required_fields:
        if field not in request_dict:
            result_dict.update({
                'status': 400,
                'msg': "error: field '%s' is missing" % field
            })
            if throw_exception:
                raise RuntimeError(json.dumps(result_dict, indent=4, sort_keys=True))
            return result_dict

    ecid = request_dict['ecid']
    p_device = Device.objects.filter(ecid=ecid).last()
    if not p_device:
        result_dict.update({
            'status': 404,
            'msg': "error: device '%s' not found" % ecid
        })
        if throw_exception:
            raise RuntimeError(json.dumps(result_dict, indent=4, sort_keys=True))
        return result_dict

    product_type = p_device.product_type
    hw_model = p_device.hw_model
    ios_version = request_dict['ios_version']
    ios_build = ''
    if 'ios_build' in request_dict:
        ios_build = request_dict['ios_build']
    ap_nonce = ''
    if 'ap_nonce' in request_dict:
        ap_nonce = request_dict['ap_nonce']
    is_ota = False
    if 'ota' in request_dict:
        is_ota = True
    should_replace = False
    if 'replace' in request_dict:
        should_replace = True

    p_signature = Signature.objects.filter(device__ecid=ecid, blob_version=ios_version, blob_build=ios_build).last()
    if p_signature:
        if should_replace:
            pass
        else:
            result_dict.update({
                'status': 500,
                'msg': "error: device '%s' already got signed with %s" % (ecid, ios_version),
            })
            if throw_exception:
                raise RuntimeError(json.dumps(result_dict, indent=4, sort_keys=True))
            return result_dict

    status, sout, serr, pid, blob_path = tsschecker(ecid=ecid, product_type=product_type, hw_model=hw_model,
                                                    ios_version=ios_version, ios_build=ios_build, ap_nonce=ap_nonce,
                                                    is_ota=is_ota)
    if status != 0:
        result_dict.update({
            'status': 501,
            'msg': "error: device '%s' did not get signed with %s" % (ecid, ios_version),
            'stdout': sout,
            'stderr': serr
        })
        if throw_exception:
            raise RuntimeError(json.dumps(result_dict, indent=4, sort_keys=True))
        return result_dict

    check_result = False
    save_prefix = 'resources/'
    flist = os.listdir(save_prefix + blob_path)
    for i in range(0, len(flist)):
        fpath = os.path.join(blob_path, flist[i])
        if os.path.isfile(save_prefix + fpath):
            check_result = True
            last_comp = fpath.split('/')[-1]
            last_comp = last_comp.split('_')
            if len(last_comp) == 5:
                if len(ios_build) > 0:
                    pass
                else:
                    ios_build = last_comp[3].split('-')[-1]
                ap_nonce = last_comp[-1].split('.')[0]
            blob_path = fpath
            break

    if not check_result:
        result_dict.update({
            'status': 502,
            'msg': "error: device '%s' did not get signed with %s" % (ecid, ios_version),
            'stdout': sout,
            'stderr': serr
        })
        if throw_exception:
            raise RuntimeError(json.dumps(result_dict, indent=4, sort_keys=True))
        return result_dict

    if not p_signature:
        p_signature = Signature()
    p_signature.device = p_device
    p_signature.blob_version = ios_version
    p_signature.blob_build = ios_build
    p_signature.ap_nonce = ap_nonce
    p_signature.blob_file = os.path.join('/', blob_path)
    p_signature.is_fetched = True
    p_signature.save()

    result_dict.update({
        'status': 200,
        'msg': "succeed: device '%s' got signed with %s" % (ecid, ios_version),
        'stdout': sout,
        'stderr': serr
    })
    return result_dict


@csrf_exempt
def sign_device(request):

    if request.method != 'POST':
        return HttpResponse(json.dumps({
            'status': 400,
            'msg': "only POST is allowed"
        }), content_type='application/json')

    async = False
    if 'async' in request.POST:
        async = True

    if not async:
        return HttpResponse(json.dumps(handle_signing_task(request.POST, False)), content_type='application/json')
    else:
        result_dict = {}

        if 'job' in request.POST:
            job_id = request.POST['job']
            m_job = queues.get_queue('high').fetch_job(job_id)
            if m_job is None:
                result_dict.update({
                    'status': 404,
                    'msg': _('No such job'),
                    'job': None
                })
            else:
                result_dict.update({
                    'status': 201,
                    'msg': '',
                    'job': {
                        'id': m_job.id,
                        'is_failed': m_job.is_failed,
                        'is_finished': m_job.is_finished,
                        'result': m_job.result
                    }
                })
        else:
            queue = django_rq.get_queue('high')
            m_job = queue.enqueue(handle_signing_task, request.POST, True)
            result_dict.update({
                'status': 200,
                'msg': _('Task submitted, proceeding...'),
                'job': {
                    'id': m_job.id,
                    # 'is_failed': m_job.is_failed,
                    # 'is_finished': m_job.is_finished,
                    'result': m_job.result
                }
            })

        return HttpResponse(json.dumps(result_dict), content_type='application/json')


@csrf_exempt
def register_device(request):
    if request.method != 'POST':
        return HttpResponse(json.dumps({
            'status': 400,
            'msg': "only POST is allowed"
        }), content_type='application/json')
    required_fields = ['name', 'hw_model', 'product_type', 'ios_version', 'ecid']
    for field in required_fields:
        if field not in request.POST:
            return HttpResponse(json.dumps({
                'status': 400,
                'msg': "error: field '%s' is missing" % field
            }), content_type='application/json')
    ecid = request.POST['ecid']
    is_create = False
    p_device = Device.objects.filter(ecid=ecid).last()
    if p_device:
        is_create = False
    else:
        is_create = True
        p_device = Device()
    p_device.ecid = ecid
    p_device.name = request.POST['name']
    p_device.hw_model = request.POST['hw_model']
    p_device.product_type = request.POST['product_type']
    p_device.ios_version = request.POST['ios_version']
    if 'ios_build' in request.POST:
        p_device.ios_build = request.POST['ios_build']
    if 'generator' in request.POST:
        p_device.generator = request.POST['generator']
    p_device.save()
    if is_create:
        return HttpResponse(json.dumps({
            'status': 200,
            'msg': "succeed: device '%s' created" % ecid
        }), content_type='application/json')
    else:
        return HttpResponse(json.dumps({
            'status': 200,
            'msg': "succeed: device '%s' updated" % ecid
        }), content_type='application/json')

