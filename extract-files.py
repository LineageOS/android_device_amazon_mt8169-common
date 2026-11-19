#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/amazon/mt8169-common',
    'hardware/amazon',
    'hardware/mediatek',
    'hardware/mediatek/libmtkperf_client',
]

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'libaal_mtk',
        'libcustom_nvram',
        'libdpframework',
        'libpq_prot',
        'libteec',
    ): lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    ('vendor/bin/hw/android.hardware.keymaster@4.0-service.optee', 'vendor/lib64/libkeymaster4-v30.so',
     'vendor/lib64/libkeymaster4support-v30.so', 'vendor/lib64/libkeymaster_messages-v30.so',
     'vendor/lib64/libkeymaster_portable-v30.so', 'vendor/lib64/libpuresoftkeymasterdevice-v30.so',
     'vendor/lib64/libsoft_attestation_cert-v30.so'): blob_fixup()
        .replace_needed('libkeymaster4.so', 'libkeymaster4-v30.so')
        .replace_needed('libkeymaster4support.so', 'libkeymaster4support-v30.so')
        .replace_needed('libkeymaster_messages.so', 'libkeymaster_messages-v30.so')
        .replace_needed('libkeymaster_portable.so', 'libkeymaster_portable-v30.so')
        .replace_needed('libpuresoftkeymasterdevice.so', 'libpuresoftkeymasterdevice-v30.so')
        .replace_needed('libsoft_attestation_cert.so', 'libsoft_attestation_cert-v30.so'),
    ('vendor/lib/android.hardware.audio.common-util-v30.so', 'vendor/lib/android.hardware.audio.common@6.0-util-v30.so'): blob_fixup()
        .replace_needed('android.hardware.audio.common-util.so', 'android.hardware.audio.common-util-v30.so')
        .replace_needed('android.hardware.audio.common@6.0-util.so', 'android.hardware.audio.common@6.0-util-v30.so')
        .replace_needed('libmedia_helper.so', 'libmedia_helper-v30.so'),
    'vendor/lib/libMtkOmxVdecEx.so': blob_fixup()
        .replace_needed('libformatter.so', 'libformatter_mtk.so')
        .replace_needed('libui.so', 'libui-v30.so'),
    'vendor/lib/libformatter_mtk.so': blob_fixup()
        .fix_soname(),
    ('vendor/lib/libh264enc_sa.ca7.so', 'vendor/lib/libmp4enc_sa.ca7.so', 'vendor/lib/libmp4enc_xa.ca7.so',
     'vendor/lib/libthha.so', 'vendor/lib/libvc1dec_sa.ca7.so', 'vendor/lib/libvcodec_oal.so',
     'vendor/lib/libvp8dec_sa.ca7.so', 'vendor/lib/libvp9dec_sa.ca7.so'): blob_fixup()
        .clear_symbol_version('__aeabi_memclr')
        .clear_symbol_version('__aeabi_memclr4')
        .clear_symbol_version('__aeabi_memcpy')
        .clear_symbol_version('__aeabi_memcpy4')
        .clear_symbol_version('__aeabi_memmove')
        .clear_symbol_version('__aeabi_memset')
        .clear_symbol_version('__gnu_Unwind_Find_exidx'),
    ('vendor/lib/libnvram.so', 'vendor/lib64/libnvram.so'): blob_fixup()
        .add_needed('libbase_shim.so'),
    'vendor/lib/libui-v30.so': blob_fixup()
        .replace_needed('android.hardware.graphics.common-V1-ndk_platform.so', 'android.hardware.graphics.common-V7-ndk.so'),
    'vendor/lib64/hw/vendor.mediatek.hardware.pq@2.6-impl.so': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so'),
    ('vendor/lib64/lib3a.ae.so', 'vendor/lib64/lib3a.ae.stat.so', 'vendor/lib64/lib3a.alsflicker.so',
     'vendor/lib64/libaaa_ltm.so'): blob_fixup()
        .add_needed('liblog.so'),
    'vendor/lib64/lib3a.flash.so': blob_fixup()
        .add_needed('liblog.so')
        .add_needed('libm.so'),
    'vendor/lib64/lib3a.flicker.so': blob_fixup()
        .add_needed('libm.so'),
    ('vendor/lib64/libaalservice.so', 'vendor/lib64/libcam.utils.sensorprovider.so'): blob_fixup()
        .replace_needed('libsensorndkbridge.so', 'android.hardware.sensors@1.0-convert-shared.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'mt8169-common',
    'amazon',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
