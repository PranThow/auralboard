#define MINIAUDIO_IMPLEMENTATION
#include "./resources/miniaudio.h"

#include <iostream>
#include <string>
#include <thread>
#include <chrono>
#include <algorithm>

// 🎧 Prints CLI usage
void print_usage() {
    std::cout << "Usage: audioplay.exe <audiofile> [--vb]\n";
}

// 🔍 Find output device matching a keyword (case-insensitive)
bool find_output_device(ma_context* context, const std::string& match, ma_device_id& outId) {
    ma_device_info* playbackDevices;
    ma_uint32 playbackDeviceCount;

    if (ma_context_get_devices(context, nullptr, nullptr, &playbackDevices, &playbackDeviceCount) != MA_SUCCESS) {
        std::cerr << "❌ Failed to enumerate playback devices.\n";
        return false;
    }

    std::string matchLower = match;
    std::transform(matchLower.begin(), matchLower.end(), matchLower.begin(), ::tolower);

    for (ma_uint32 i = 0; i < playbackDeviceCount; ++i) {
        std::string name = playbackDevices[i].name;
        std::string nameLower = name;
        std::transform(nameLower.begin(), nameLower.end(), nameLower.begin(), ::tolower);

        if (nameLower.find(matchLower) != std::string::npos) {
            std::cout << "🔊 Found matching output device: " << name << "\n";
            outId = playbackDevices[i].id;
            return true;
        }
    }

    return false;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        print_usage();
        return 1;
    }

    std::string filePath;
    bool useVBCable = false;

    // 📦 Parse CLI args
    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "--vb") {
            useVBCable = true;
        } else if (filePath.empty()) {
            filePath = arg;
        }
    }

    if (filePath.empty()) {
        print_usage();
        return 1;
    }

    // 🛠️ Setup audio context
    ma_context context;
    if (ma_context_init(nullptr, 0, nullptr, &context) != MA_SUCCESS) {
        std::cerr << "❌ Failed to initialize miniaudio context.\n";
        return -1;
    }

    ma_engine_config config = ma_engine_config_init();
    config.pContext = &context;

    // 🧩 Select VB-Cable output if requested
    if (useVBCable) {
        ma_device_id vbId{};
        if (find_output_device(&context, "vb-audio", vbId)) {
            config.pPlaybackDeviceID = &vbId;
        } else {
            std::cerr << "⚠️ VB-Cable device not found. Using default output.\n";
        }
    }

    // 🎛️ Initialize engine
    ma_engine engine;
    if (ma_engine_init(&config, &engine) != MA_SUCCESS) {
        std::cerr << "❌ Failed to initialize audio engine.\n";
        ma_context_uninit(&context);
        return -1;
    }

    // 🎶 Load and play sound
    ma_sound sound;
    if (ma_sound_init_from_file(&engine, filePath.c_str(), 0, nullptr, nullptr, &sound) != MA_SUCCESS) {
        std::cerr << "❌ Failed to load audio file: " << filePath << "\n";
        ma_engine_uninit(&engine);
        ma_context_uninit(&context);
        return -1;
    }

    std::cout << "▶️ Playing: " << filePath << "\n";
    ma_sound_start(&sound);

    while (ma_sound_is_playing(&sound)) {
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }

    std::cout << "✅ Playback finished.\n";

    ma_sound_uninit(&sound);
    ma_engine_uninit(&engine);
    ma_context_uninit(&context);
    return 0;
}
