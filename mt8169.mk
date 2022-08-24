#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

# Non_ab_device
$(call inherit-product, $(SRC_TARGET_DIR)/product/non_ab_device.mk)

# Dynamic Partitions
PRODUCT_USE_DYNAMIC_PARTITIONS := true

# Rootdir
PRODUCT_PACKAGES += \
    fstab.emmc \
    fstab.emmc.vendor_ramdisk

# Soong namespaces
PRODUCT_SOONG_NAMESPACES += \
    $(LOCAL_PATH)

# Verified Boot
PRODUCT_PACKAGES += \
    android.software.verified_boot.prebuilt.xml

# Inherit the proprietary files
$(call inherit-product, vendor/amazon/mt8169-common/mt8169-common-vendor.mk)
