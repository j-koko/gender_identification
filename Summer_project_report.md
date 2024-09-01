# Summer Project Report

# Methodology

While inferring gender based solely on voice pitch is less reliable than modern state-of-the-art techniques, fundamental frequency remains an important differentiator between adult male and female voices. Various sources provide different pitch ranges oscillating around 95 Hz \- 155 Hz for males and 184 Hz \- 243 Hz for females \[1\]. Binary classification requires a single threshold, so I initially selected the upper range for male 155 Hz as the cutoff point, classifying any voice recording above this threshold as female. These values from the literature were used as the initial threshold in the current script. However, recognizing that this threshold might not yield the highest accuracy in gender recognition, I sought a dataset to test and validate the script's performance.

## Testing Gender Inference on an Annotated Dataset

The AudiMNIST dataset consists of 30,000 audio recordings of cardinal numbers, recorded by 60 different speakers \[2\]. In the original dataset, each folder contains multiple recordings of numbers spoken by the same individual. For the purposes of this experiment, only one recording per speaker was required. Therefore, the first recording from each folder was extracted, resulting in a new dataset of 60 recordings in total. Subsequently, the metadata from the original dataset including information on gender, was utilized in a script named `test.py` to assess the accuracy of the algorithm and to make any necessary adjustments.

## Experimenting with Threshold Values

Initially, the average pitch was calculated from a list of frequencies greater than zero. If the average pitch exceeded 155 Hz, the script classified the gender as female. The following table summarizes the results obtained for different thresholds:

| Threshold (average pitch in Hz) | Correct inferences | Accuracy (%) |
| :---- | :---- | :---- |
| 155 Hz | 47 out of 60 | 78.33% |
| 160 Hz | 48 out of 60 | 80% |
| 165 Hz  | 49 out of 60 | 81.66% |
| 180 Hz | 51 out of 60 | 85% |
| 190 Hz | 50 out of 60 | 83.33% |
| 200 Hz | 49 out of 60 | 81.66% |

To improve the accuracy, I subsequently filtered out frequencies likely to be non-human speech (i.e., below 60 Hz and above 300 Hz). The results for the same dataset after filtering are as follows:

| Threshold (average pitch in Hz) | Correct inferences | Accuracy (%) |
| :---- | :---- | :---- |
| 155 Hz | 55 out of 60 | 91.66% |
| 160 Hz | 57 out of 60 | 95% |
| 165 Hz  | 57 out of 60 | 95% |
| 180 Hz | 58 out of 60 | 96.66% |
| 190 Hz | 57 out of 60 | 95% |
| 200 Hz | 56 out of 60 | 93.33% |

Filtering out non-speech frequencies significantly increased the accuracy of the script, with 180 Hz emerging as the most accurate threshold. However, this approach has limitations that must be considered.

# Biases in the Methodology

The first limitation is the significant imbalance in the dataset's gender ratio, with 48 male speakers and only 12 female speakers. As a result, a higher frequency threshold (180 Hz) yields the best results for this particular dataset because the small number of female speakers reduces the likelihood of encountering extreme (atypical) frequency values for that gender (below 180 Hz). The two misclassifications in the final version of the script (using the 180 Hz threshold and after filtering non-speech frequencies) were both female speakers with lower-pitched voices who were incorrectly classified as male. Consequently, the same script would likely have a considerably lower accuracy rate with a dataset that includes a more balanced female-to-male ratio.

The second limitation is that the script provides only binary classification, meaning that any speakers who identify as neither female nor male (non-binary) will not be classified correctly. While their voices might display characteristics of either gender, the classification result would not accurately represent their self-identified gender.

Additionally, the script is not suitable for children, as their fundamental frequency ranges from 244 Hz (182–331 Hz) in girls and 250 Hz (205–293 Hz) in boys \[3\]. As a result, boys would likely be incorrectly recognized as female speakers.

# Ethical Considerations

The first ethical consideration is the need for inclusivity in such systems. A binary gender recognition system is inherently non-inclusive, as it may consistently misidentify non-binary individuals as either male or female, failing to represent their true gender identity. This misclassification can have practical consequences in real-life scenarios, such as denying someone access to gender-specific facilities like public restrooms. Beyond practical implications, these misrecognitions can also impose an emotional burden on the individuals affected, who may feel judged and categorized by an algorithm. Therefore, it is crucial to design such systems with sensitivity to these issues.

Furthermore, it is essential to handle personal information in compliance with data privacy regulations. While gender itself may not be classified as sensitive personal data, it can be combined with other information to identify individuals, making techniques like pseudonymization valuable when managing such data. Gender recognition systems must adhere to both data privacy and anti-discrimination laws to ensure ethical operation.

Transparency is another important consideration. Users should be informed about how their gender was inferred and should have the option to challenge the algorithm's decision. In this script, for example, users are provided with the average pitch of their voice, which is the basis for the gender inference.

Finally, such systems should be designed if their use benefits the society or serves educational purposes and as such is ethically justifiable. It is important to avoid deploying gender recognition systems for trivial or potentially harmful purposes.

# Bibliography

\[1\] Tielen MT. Fundamental Frequency Characteristics of Middle Aged Men and Women . 1989\.

\[2\] Becker S, Vielhaben J, Ackermann M, Müller K, Lapuschkin S, Samek W. AudioMNIST: Exploring Explainable Artificial Intelligence for audio analysis on a simple benchmark. Journal of the Franklin Institute 2024;361(1):418–428.

\[3\] Linders B, Massa GG, Boersma B, Dejonckere PH. Fundamental voice frequency and jitter in girls and boys measured with electroglottography: influence of age and height. Int J Pediatr Otorhinolaryngol 1995;33(1):61–65.
