/*
 * SPDX-FileCopyrightText: The LineageOS Project
 * SPDX-License-Identifier: Apache-2.0
 */

#define LOG_TAG "aemgr_shim"

#include <dlfcn.h>
#include <log/log.h>

#include <cstdint>

namespace NS3Av3 {

class AeMgr {
  public:
    int32_t setAEMinMaxFrameRate(int32_t minFps, int32_t maxFps);
};

namespace {

using SetAEMinMaxFrameRate = int32_t (*)(AeMgr*, int32_t, int32_t);

// Frame rates are in fps * 1000.
constexpr int32_t kMaxFixedFps = 30000;
constexpr int32_t kMinLowLightFps = 15000;

SetAEMinMaxFrameRate GetSetAEMinMaxFrameRate() {
    void* handle = dlopen("libcam.hal3a.v3.ae.so", RTLD_NOW | RTLD_NOLOAD);
    if (!handle) {
        ALOGE("Failed to find libcam.hal3a.v3.ae.so: %s", dlerror());
        return nullptr;
    }

    return reinterpret_cast<SetAEMinMaxFrameRate>(
            dlsym(handle, "_ZN6NS3Av35AeMgr20setAEMinMaxFrameRateEii"));
}

}  // namespace

int32_t AeMgr::setAEMinMaxFrameRate(int32_t minFps, int32_t maxFps) {
    static const SetAEMinMaxFrameRate setAEMinMaxFrameRate = GetSetAEMinMaxFrameRate();

    if (minFps == maxFps && minFps > kMinLowLightFps && maxFps <= kMaxFixedFps) {
        minFps = kMinLowLightFps;
    }

    return setAEMinMaxFrameRate ? setAEMinMaxFrameRate(this, minFps, maxFps) : -1;
}

}  // namespace NS3Av3
