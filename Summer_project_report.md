# Gender Prediction from Voice Pitch 

1. ## Introduction

The goal of this project was to develop a Python script capable of predicting gender based on a speaker's fundamental frequency (pitch). The script is designed for binary gender classification, categorizing speakers as either male or female.

Initially, I understood that men generally have a lower fundamental frequency than women, and I assumed there was little overlap in pitch ranges between the two genders. This seemed to explain why we can often distinguish between male and female voices with ease. However, through further research and analysis, I realized that while this is true for many speakers, it is not universally applicable.

Before starting my studies, I completed over 100 hours of MOOC programming courses. Using this foundation, I developed several personal projects, such as GUI games, a Pomodoro timer, and a brick calculator. Some of my projects were related to linguistics, including a basic phonetic transcription program for Polish, which, though incomplete, provided an interesting challenge.

In my current role as a computational linguist, I use Python to automate tasks. Although I have limited experience in audio processing, my responsibilities in the TTS team involve frontend tasks like text normalization, grapheme-to-phoneme transcription, and evaluating acoustic models. However, I have not previously processed audio files programmatically, despite working with them in other capacities.

## 2\. Methodology

### 2.1 Intended approach

Before this project, I had no prior experience with the pyaudio and wave libraries, so I used large language models (LLMs) to generate the initial structure for the record\_audio function. Afterward, I researched online to better understand the methods and their parameters, such as mono and stereo channels, common sampling rates, and audio encoding formats. I chose to record 5 seconds of speech, as this provides enough time to capture a simple sentence.

For pitch analysis, I knew from the outset that I wanted to extract the average pitch from each utterance. Having previously worked with Praat, I found it easier to use the parselmouth library for this task compared to learning pyaudio or wave.

While inferring gender based solely on voice pitch is less reliable than modern state-of-the-art techniques, fundamental frequency remains an important differentiator between adult male and female voices. Various sources provide different pitch ranges oscillating around 95 Hz \- 155 Hz for males and 184 Hz \- 243 Hz for females (Tielen, 1989). Binary classification requires a single threshold, so I initially selected the upper range for male 155 Hz as the cutoff point, classifying any voice recording above this threshold as female. These values from the literature were used as the initial threshold in the current script. However, recognizing that this threshold might not yield the highest accuracy in gender recognition, I sought a dataset to test and validate the script's performance.

### 2.2 Data collection

The AudiMNIST dataset consists of 30,000 audio recordings of cardinal numbers, recorded by 60 different speakers (Becker et al., 2024). In the original dataset, each folder contains multiple recordings of numbers spoken by the same individual. For the purposes of this experiment, only one recording per speaker was required. Therefore, the first recording from each folder was extracted, resulting in a new dataset of 60 recordings in total. Subsequently, the metadata from the original dataset including information on gender, was utilized in a script named test.py to assess the accuracy of the algorithm and to make any necessary adjustments.

One of the challenges I faced was cleaning the dataset. Specifically, I needed to extract the first file from each folder. Since I had never used the shutil library before, I consulted a large language model (LLM) to generate a simple script that would accomplish this task.

## 3\. Results

## Initially, the average pitch was calculated from a list of frequencies greater than zero. If the average pitch exceeded 155 Hz, the script classified the gender as female. The following table summarizes the results obtained for different thresholds:

| Threshold (average pitch in Hz) | Correct inferences | Accuracy (%) |
| :---- | :---- | :---- |
| 155 Hz | 47 out of 60 | 78.33% |
| 160 Hz | 48 out of 60 | 80% |
| 165 Hz  | 49 out of 60 | 81.66% |
| 180 Hz | 51 out of 60 | 85% |
| 190 Hz | 50 out of 60 | 83.33% |
| 200 Hz | 49 out of 60 | 81.66% |

To improve the accuracy, I subsequently filtered out frequencies that were unlikely to be human speech (i.e., below 60 Hz and above 300 Hz). The results for the same dataset after filtering are as follows:

| Threshold (average pitch in Hz) | Correct inferences | Accuracy (%) |
| :---- | :---- | :---- |
| 155 Hz | 55 out of 60 | 91.66% |
| 160 Hz | 57 out of 60 | 95% |
| 165 Hz  | 57 out of 60 | 95% |
| 180 Hz | 58 out of 60 | 96.66% |
| 190 Hz | 57 out of 60 | 95% |
| 200 Hz | 56 out of 60 | 93.33% |

Filtering out non-speech frequencies significantly increased the accuracy of the script, with 180 Hz emerging as the most accurate threshold. However, this approach has limitations that must be considered.

## 4\. Discussion

### 4.1 Biases in the methodology

The first limitation is the significant imbalance in the dataset's gender ratio, with 48 male speakers and only 12 female speakers. As a result, a higher frequency threshold (180 Hz) yields the best results for this particular dataset because the small number of female speakers reduces the likelihood of encountering extreme (atypical) frequency values for that gender (below 180 Hz). The two misclassifications in the final version of the script (using the 180 Hz threshold and after filtering non-speech frequencies) were both female speakers with lower-pitched voices who were incorrectly classified as male. Consequently, the same script would likely have a considerably lower accuracy rate with a dataset that includes a more balanced female-to-male ratio.

The second limitation is that the script provides only binary classification, meaning that any speakers who identify as neither female nor male (non-binary) will not be classified correctly. While their voices might display characteristics of either gender, the classification result would not accurately represent their self-identified gender.

Additionally, the script is not suitable for children, as their fundamental frequency ranges from 244 Hz (182–331 Hz) in girls and 250 Hz (205–293 Hz) in boys (Linders et al., 1995). As a result, boys would likely be incorrectly recognized as female speakers.

### 4.2 Ethical considerations

The first ethical consideration is the need for inclusivity in such systems. A binary gender recognition system is inherently non-inclusive, as it may consistently misidentify non-binary individuals as either male or female, failing to represent their true gender identity. This misclassification can have practical consequences in real-life scenarios, such as denying someone access to gender-specific facilities like public restrooms. Beyond practical implications, these misrecognitions can also impose an emotional burden on the individuals affected, who may feel judged and categorized by an algorithm. Therefore, it is crucial to design such systems with sensitivity to these issues.

Furthermore, it is essential to handle personal information in compliance with data privacy regulations. While gender itself may not be classified as sensitive personal data, it can be combined with other information to identify individuals, making techniques like pseudonymization valuable when managing such data. Gender recognition systems must adhere to both data privacy and anti-discrimination laws to ensure ethical operation.

Transparency is another important consideration. Users should be informed about how their gender was inferred and should have the option to challenge the algorithm's decision. In this script, for example, users are provided with the average pitch of their voice, which is the basis for the gender inference.

Finally, such systems should be designed if their use benefits the society or serves educational purposes and as such is ethically justifiable. It is important to avoid deploying gender recognition systems for trivial or potentially harmful purposes.

### 4.4 Future improvements

The next step would be to add a function that prompts the user to confirm whether the inferred gender matches their self-identified gender, then saves the recording in the data folder and the annotated gender in the metadata in test.py. This approach would allow the dataset to grow with each new recording. For example, testing the script with classmates could increase the dataset size by nearly 50%, helping to address the male-female ratio bias.

Alternatively, an approach that incorporates additional features such as Mel-frequency cepstral coefficients (MFCCs) or energy, along with pitch, could be explored to improve accuracy (Chaudhary & Sharma, Oct 2018).

## 5\. Conclusion

This project has significantly deepened my understanding of voice technology, particularly the numerous factors involved in processing a seemingly simple audio file. While I do not yet fully grasp all the technical details of audio processing, I now have a far greater understanding than I did before. I also learned how much methodology can influence outcomes; for example, a small adjustment, like filtering out non-voice frequencies, led to more reliable results. Interestingly, this idea came to me not while working, but during my leisure time—something that often happens in programming.

My familiarity with Python libraries such as pyaudio, wave, and parselmouth, as well as Python control flow, improved throughout the project. Most importantly, this experience has changed how I view myself. Previously, I saw myself primarily as a linguist and felt apprehensive about the technical aspects of my MSc in Voice Technology. However, successfully completing this project with a high accuracy rate has boosted my confidence and strengthened my determination to continue pursuing this degree and advancing in the voice technology field.

### References (correct references)

Becker, S., Vielhaben, J., Ackermann, M., Müller, K., Lapuschkin, S., & Samek, W. (2024). AudioMNIST: Exploring Explainable Artificial Intelligence for audio analysis on a simple benchmark. *Journal of the Franklin Institute, 361*(1), 418–428. 10.1016/j.jfranklin.2023.11.038

Chaudhary, S., & Sharma, D. K. (Oct 2018). Gender Identification based on Voice Signal Characteristics. Paper presented at the 869–874. 10.1109/ICACCCN.2018.8748676 [https://ieeexplore.ieee.org/document/8748676](https://ieeexplore.ieee.org/document/8748676)

Hoefsloot, M. E. (2021). *an Inquiry Into the Ethics of Automatic Gender Recognition Photo by Quino Al on Unsplash*

Linders, B., Massa, G. G., Boersma, B., & Dejonckere, P. H. (1995). Fundamental voice frequency and jitter in girls and boys measured with electroglottography: influence of age and height. *International Journal of Pediatric Otorhinolaryngology, 33*(1), 61–65. 10.1016/0165-5876(95)01197-J

Tielen, M. T. (1989). *Fundamental Frequency Characteristics of Middle Aged Men and Women* 