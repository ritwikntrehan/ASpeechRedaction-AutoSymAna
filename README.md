# ASpeechRedaction-AutoSymAna
The Architecture, Revisited
As a brief re-introduction to the problem, we are building a system that will join the suite of symptom monitoring automation. To address concerns over the privacy of adults in the infant patient’s vicinity, we want to pre-emptively redact any instance of adult speech during audio recording.

In order to accomplish this, we set up the architecture so that a live-stream of audio is processed with a speech detection module and appropriately redacted before storage of the live-streamed audio. Below, we detail our method for the actions this architecture is expected to complete and our response to the constraints on the architecture.

Actions
Retrieve and Process Audio Stream
The architecture must bring in a live-stream of audio at 128kbps AAC. This process is a standard method of converting audio data into a machine-readable format. So, the audio is first decoded from AAC into PCM. Significant and unusual moments in the audio are highlighted for increased processing. The audio is then chunked into iterative and overlapping pieces of audio. This ensures a lower computational effect with a higher level of processing accuracy.  

The chunk of audio data is then “Feature Extracted”. Crucial audio data features, named Mel-frequency cepstral coefficients (MFCCs), are calculated for each chunk. This processing will translate the audio for the machine learning model to detect adult speech.
Redact Predicted Adult Speech
Once we have our audio stream segmented, we leverage one of our selected speech detection AI models to locate times with speech within each chunk of audio data. Identified adult speech segments are then redacted from the audio stream through a process named “Audio Destruction”, namely overwriting the audio with silence. This ensures the original audio is irretrievable. It also maintains an uninterrupted flow of the audio recording. Therefore, all other sensors and information gathering devices will still be synchronized with each other. This method provides privacy without compromising the integrity of the remaining recording.
Listen to babies
This system is being used while we are monitoring infant patients. In order to not falsely flag diagnostic audio data as having adult speech, as could be the case if using volume or pitch thresholds, we rely on the ability of pre-trained speech recognition models. Infants are unable to write sentences in some cases until 30 months of age. Their use of words begins sometime in their first year. So in younger patients, a speech recognition software like speech-to-text will be able to disregard the communicative vocalizations of an infant. 
Remove Audio Data of Adults
The audio redaction process relies on a stable state technique. This means that on the first detection of adult speech, the audio begins recording as silence. After sufficient return to standard environmental audio, meaning that the system interprets the adult speech to have ceased, then the recording proceeds as standard. The use of smaller chunks allows the system to react quickly, and the spare memory allows the system to retroactively write over a few seconds of previously processed but unstored data. The retroactive overwriting acts as a safety measure, a buffer between the adults’ speech.
Ignore Environment
The environmental noises are another reason why there must be a nuanced approach to redacting audio. Volume thresholds and frequency filters will cause a higher number of false negatives in the infant audio monitoring. The speech recognition models we are relying on are trained to be used in casual and pedestrian use cases, meaning that there will be settings with high amounts of background noises. By focusing on only the speech of adults, we remove the concern of overwriting data unnecessarily. 
Store Audio Data
Once the adult speech has been removed from the audio stream, the redacted audio will be safely stored in an S3 bucket. While this can be performed, it is also possible to store the data locally. The purpose of this would be to perform post-processing on the audio data; for example, symptom assessment on the infant audio data, like identifying crying fits. Either storage solution ensures reliable and secure access to the processed audio for further analysis and utilization, allowing extraction of valuable diagnostic insights.

Constraints
There are several constraints to uphold when constructing our system. These center around data types, computational style, technological adaptability, and success.
Audio Format
As of now, the software architecture that has been put in place makes use of AAC data. The change to other data formats like mp3 is shown to be possible with secondary functions. Moreso, the architecture is built around accepting live-streams of audio and processing that data in real time, as we want immediate redaction of the audio.
Operational Efficiency
AI Model Computation RAM
The operational efficiency has been held as a backbone to this system since inception. The two options for the speech detection AI are set to run at or below the ideal threshold of 500MB of RAM, with potential to operate nearer to 1/10th of that. 
Stable State Technique
Speech detection algorithms operate continuously, analyzing every audio frame. This constant processing can be computationally expensive, especially for resource-constrained devices. The Stable State approach reduces the workload. Once adult speech is detected, the system halts all audio detection, and begins searching for silence.

Then the relevant portions of the audio are muted, minimizing unnecessary redaction and preserving the integrity of the remaining recording. Continuous processing can lead to increased latency, affecting the real-time responsiveness of the system. The Stable State approach reduces latency by minimizing unnecessary processing, reduces memory consumption by using data subsets, and can then be deployed on a larger scale with reduced bottlenecks.
Thresholded Initialization
"Thresholded Initialization" reduces unnecessary processing by only activating the processing pipeline when the audio deviates significantly from a previously established baseline. By only processing audio exceeding a predetermined threshold, we allow a reduction of system workload. Without thresholding, a traditional approach would continuously analyze all incoming audio, even during relative silence.

The method provides the same benefits of reduced latency, memory consumption, and bottlenecks.

When translating software from python into Android, there are necessary adjustments for language syntax, libraries, and processing. All libraries were selected so that an appropriate Android library could be implemented in the Android development. There is also the need to adjust python-specific data structures like lists, python specific syntax for the loops and indentations. Another task is to include processing techniques like multi-threading and other computational optimizations. 
When designing the python architecture, I selected AI models and methods that would allow us to begin with an incredibly efficient starting point. This will mean that inclusion of those delicate processing techniques will allow for an even further optimization. In other words, these techniques become an optional bonus for increased efficiency rather than a requirement for this framework to be adaptable to an Android port.

