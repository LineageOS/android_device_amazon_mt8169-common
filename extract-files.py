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
    ('vendor/lib/libnvram.so', 'vendor/lib64/libnvram.so'): blob_fixup()
        .add_needed('libbase_shim.so'),
    'vendor/lib64/hw/vendor.mediatek.hardware.pq@2.6-impl.so': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so'),
    'vendor/lib64/libaalservice.so': blob_fixup()
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
