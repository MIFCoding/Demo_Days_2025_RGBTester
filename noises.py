import numpy as np

rng = np.random.default_rng()


def add_gaussian_noise(audio: np.ndarray, mean: float = 0.0, sigma: float = 0.2) -> np.ndarray:
    if audio.dtype != np.float32:
        audio = audio.astype(np.float32) / np.iinfo(audio.dtype).max
    noise = rng.normal(mean, sigma, size=audio.shape).astype(np.float32)
    noisy = np.clip(audio + noise, -1.0, 1.0)
    return noisy


def add_white_noise(audio: np.ndarray, snr_db: float) -> np.ndarray:
    power_signal = np.mean(audio ** 2)
    power_noise = power_signal / (10 ** (snr_db / 10))
    noise = rng.normal(0.0, np.sqrt(power_noise),
                       size=audio.shape).astype(np.float32)
    return np.clip(audio + noise, -1.0, 1.0)


def add_impulse_noise(audio: np.ndarray, probability: float = 0.01, amplitude: float = 0.5) -> np.ndarray:
    mask = rng.random(size=audio.shape) < probability

    noise = np.zeros_like(audio)
    noise[mask] = amplitude * rng.choice([-1, 1], size=np.sum(mask))

    return np.clip(audio + noise, -1.0, 1.0)


def add_reverb(audio: np.ndarray, delay: float = 0.3, decay: float = 0.5, num_echos: int = 3) -> np.ndarray:
    delay_samples = int(delay * 44_100)
    output = np.copy(audio)

    for i in range(1, num_echos + 1):
        decay_factor = decay ** i
        echo_signal = np.roll(audio, i * delay_samples) * decay_factor

        echo_signal[:i * delay_samples] = 0
        output += echo_signal

    return np.clip(output, -1.0, 1.0)


def add_tonal_noise(audio: np.ndarray, freq: float = 1000.0, amplitude: float = 0.1) -> np.ndarray:
    t = np.arange(len(audio)) / 44_100
    noise = amplitude * np.sin(2 * np.pi * freq * t)
    return np.clip(audio + noise, -1.0, 1.0)


def add_ac_hum(audio: np.ndarray, base_freq: float = 50.0, amplitude: float = 0.1, num_harmonics: int = 3) -> np.ndarray:
    t = np.arange(len(audio)) / 44_100
    noise = np.zeros_like(audio)

    for i in range(1, num_harmonics + 1):
        harmonic_freq = base_freq * i
        noise += amplitude * np.sin(2 * np.pi * harmonic_freq * t) / i

    return np.clip(audio + noise, -1.0, 1.0)
