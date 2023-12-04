# -*- coding: utf-8 -*-
"""Framework.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LvWY5TeUXNNoNC_tH54-MatiQoFomwfC
"""

import PyAudio
import numpy as np
import librosa
import subprocess
import mp3
import boto3

class AudioPreprocessor:
    def __init__(self, sample_rate=16000, frame_size=0.02, frame_overlap=0.01):
        self.sample_rate = sample_rate
        self.frame_size = sample_rate * frame_size
        self.frame_overlap = sample_rate * frame_overlap
        self.pre_emphasis_coeff = 0.97

def decode_aac(self, audio_stream): # Decodes AAC audio stream to PCM data using ffmpeg.  Args: audio_stream (bytes): The raw AAC audio data.  Returns: numpy.ndarray: The decoded PCM audio data.
    # Create a temporary file to store the AAC data
    with tempfile.NamedTemporaryFile(suffix=".aac") as f:
        f.write(audio_stream)
        f.flush()
        # Use ffmpeg to decode the AAC file to PCM
        pcm_data = subprocess.check_output(["ffmpeg", "-i", f.name, "-f", "s16le", "-ar", str(self.sample_rate), "-ac", "1", "-"]).astype(np.int16)
        #pcm_data = subprocess.check_output(["ffmpeg", "-i", f.name, "-f",
        #"s16le", "-ar", str(self.sample_rate), "-ac", "1", "-"]).astype(np.int16)
    return pcm_data

def decode_mp3(audio_data): #like decode_aac for mp3
    # Create an MP3 decoder object
    decoder = mp3.MP3(audio_data)
    # Decode the MP3 data
    pcm_data = decoder.read_frames(decoder.info.length)
    # Convert the decoded data to a NumPy array
    decoded_audio = np.frombuffer(pcm_data, dtype=np.int16)
    return decoded_audio

    def pre_emphasis(self, audio_data):
        # Apply pre-emphasis filter to boost high frequencies
        pre_emphasized_data = np.zeros_like(audio_data)
        pre_emphasized_data[1:] = audio_data[1:] - self.pre_emphasis_coeff * audio_data[:-1]
        return pre_emphasized_data

    def frame_audio(self, audio_data):
        # Frame audio into overlapping segments
        frames = []
        for i in range(0, len(audio_data) - self.frame_size + self.frame_overlap, self.frame_overlap):
            frame = audio_data[i:i + self.frame_size]
            # Apply window function (e.g., Hamming window) if necessary
            frames.append(frame)
        return frames

def get_mfccs(self, audio_data): # Computes Mel-frequency cepstral coefficients (MFCCs) for each frame. Args: audio_data (numpy.ndarray): The audio data in PCM format. Returns: numpy.ndarray: The MFCCs for each frame.
    mfccs = []
    # Divide audio into frames with overlap
    for frame in self.frame_audio(audio_data):
        # Compute MFCCs for the frame
        mfcc = librosa.feature.mfcc(frame, sr=self.sample_rate, n_mfcc=self.num_ceps)
        mfccs.append(mfcc.T)
    return np.stack(mfccs)


    def preprocess(self, audio_stream):
        # Decode AAC stream
        audio_data = self.decode_aac(audio_stream)

        # Apply pre-emphasis filter
        audio_data = self.pre_emphasis(audio_data)

        # Frame audio into overlapping segments
        frames = self.frame_audio(audio_data)

        # Compute MFCCs for each frame
        mfccs = self.get_mfccs(frames)

        # Return MFCCs and other relevant features (e.g., delta, delta-delta)
        return mfccs

class FeatureExtractor:
    def __init__(self, num_ceps=13, delta_order=2):
        self.num_ceps = num_ceps
        self.delta_order = delta_order

    def extract_features(self, mfccs):
        # Extract relevant features from MFCCs
        features = []
        for i in range(len(mfccs)):
            # Feature vector includes MFCCs
            feature_vector = mfccs[i]

            # Optionally include delta and delta-delta features
            for order in range(1, self.delta_order + 1):
                delta_mfccs = np.diff(mfccs[max(i - order, 0):i + order + 1], axis=0)
                feature_vector = np.concatenate((feature_vector, delta_mfccs[-1]))
            features.append(feature_vector)
        return features

    def normalize_features(self, features):
        # Apply feature normalization
        mean = np.mean(features, axis=0)
        std = np.std(features, axis=0)
        normalized_features = (features - mean) / std
        return normalized_features

  class SpeechDetectionModel:
    def __init__(self, model_path):
        # Load the chosen speech detection model based on your selection

    def predict(self, features):
        # Predict the probability of speech for each feature vector
        predictions = []
        for feature_vector in features:
            # Pass feature vector to the model for prediction
            # ...
            prediction = # Model's output (e.g., probability of speech)
            predictions.append(prediction)
        return predictions

class SpeechDecisionMaker:
    def __init__(self, threshold=0.5):
        self.threshold = threshold

    def classify_speech(self, predictions):
        # Classify each frame as speech or non-speech based on prediction and threshold
        speech_frames = []
        for prediction in predictions:
            if prediction > self.threshold:
                speech_frames.append(True)
            else:
                speech_frames.append(False)
        return speech_frames

    def detect_speech_segments(self, speech_frames, min_duration=0.5):
        # Detect speech segments using a simple state machine
        in_speech = False
        speech_segments = []
        current_segment = []

        for i, frame in enumerate(speech_frames):
            if not in_speech and frame:
                # Speech onset detected
                in_speech = True
                current_segment.append(i)
            elif in_speech and not frame:
                # Speech offset detected
                in_speech = False
                if len(current_segment) >= min_duration * self.frame_rate:
                    speech_segments.append(current_segment)
                current_segment = []

        # Check for unfinished segment at the end
        if in_speech and len(current_segment) >= min_duration * self.frame_rate:
            speech_segments.append(current_segment)

        return speech_segments

def silence_speech_segments(audio_data, speech_segments): #Overwrites speech segments with silence in an audio stream.  Args:   audio_data (numpy.ndarray): The audio data in PCM format. speech_segments (list): A list of speech segments, where each segment is a tuple of (start_frame, end_frame). Returns: numpy.ndarray: The modified audio data with speech segments replaced by silence.
    for segment in speech_segments:
        start_frame = segment[0]
        end_frame = segment[1]
        silence = np.zeros_like(audio_data[start_frame:end_frame])
        audio_data[start_frame:end_frame] = silence
    return audio_data