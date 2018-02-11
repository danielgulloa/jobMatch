The process of looking for a new job is in itself a full-time job. There is an overwhelming amount of job postings and many times it is difficult to determine which jobs are the best matches to your skills and preferences. It is important to do some research about the jobs before applying and furthermore, before accepting a job offer. On the other hand, job postings also receive an overwhelming amount of applications, and it is well-known[citation needed] that the companies use Application Tracking Systems (ATS) to weed out those candidates that are not a good match for the job. The basic idea is that the ATS searches the applicant's resume for predetermined keywords and for a particular language (mostly hard and soft skills) and then only saves those resumes with the highest match. For this reason, each time that you want to apply for a job, you should change your resume to emphasize those things that the company is looking for. To put an example, if I am looking into a data science job, I should emphasize the work that I have done working with data, while if it is a machine learning job, then I should emphasize in my resume the machine learning algorithms that I have used. This all sounds simple enough, and it sounds that you would just need a small set of resumes and use a different one for each type of job. However, the job postings are all different, and some of them use some words more than others, and your resume should match that language too.
To help job seekers "beat" the ATS, I have developed a python program that 1) looks for hard skills (e.g. "Python", "Programming") and soft skills (e.g. "Communication", "Team Work") in a job description and in your current resume, and tells you how many times it is mentioned on each, and 2) Looks for the common words or phrases that are used in the job description (e.g. "data","experience","excellent") and tells you how many times it is written in the job description and how many times it is written in your resume. Given this data, the goal is to modify your resume to look as similar as possible to the job description.
If you would like to try it out, all you would need to do is download the code from my github (github.com/danielgulloa/jobMatch), make a txt file with the job description, and make a txt file with your resume. Put all of the files in the same folder, and then run Keyword_Extractor.py entering the job description file and the resume as parameters in standard input. In other words:

Copy the job description in a txt file and save it with a descriptive name (e.g. tesla_job_description.txt). Do the same with your resume (e.g. my_resume.txt).

$git clone https://github.com/danielgulloa/jobMatch

$cp tesla_job_description.txt my_resume.txt jobMatch

$python Keyword_Extractor.py tesla_jobdescription.txt my_resume.txt

A file will be created, called Extracted_Keywords.csv, which will have 7 columns and many rows. Here are the first 6 rows of an example I ran:

,type,skill,job,cv,m1,m2

55,soft,experience,5,2,3,3

60,general,one,5,0,5,5

63,general,learning,4,3,1,1

17,hard,apache,4,1,3,3

40,hard,data,3,15,-12,0


The first column is just an index, then the second one is the type of skill ("hard","soft", or "general" for general language in the job description). The third column is the name of the skill, then the fourth is how many times the skill appears in the job description, and the fifth is how many times it appears in your resume. The rows in the file are sorted by 'job' and then by 'cv'. The last two columns are a "distance" measure. m1 is simply (job - cv), which tells you how many more times the skill appears in the job description than in the resume. This value could be negative (hence the quotation marks on "distance"), and the goal is to have the sum of m1 as small (or negative) as possible. The value of m2 is obtained as max(0,job-cv). In this case, adding the skill many times in your resume does not increase the overall similarity between the job description and the resume. If you have different ideas on what measures to include, please let me know to include them in the github version.

The program can be easily modified to suit individual needs. The download consists mainly of the Keyword_Extractor.py program and two files: hardskills.txt and softskills.txt. These lasts two files contains a relatively small list of hard and soft skills, and it is meant for people looking for jobs in information technology. In particular, hardskills.txt should be modified for other industries. You can easily add or remove skills from these files. The order does not matter, nor is it important if there are repeated skills; the program will get rid of duplicates (function load_skills). Furthermore, capitalizations and punctuation marks are also removed (function clean_phrase), both from the skills and the job description. This way, something like "Self-driven" will be considered the same as "selfdriven".

The program considers key-phrases, which consists of one (keyword or mono-gram), two (bi-gram), or three (tri-gram) words. The function build_ngram_distribution can be easily modified to consider as many n-grams as needed, but short key-phrases work best.

In the case of the general language, we are only interested in the relevant parts of speech, so the program removes unimportant words such as conjunctions or interjections, and keeps only nouns, verbs, adjectives, and adverbs. Some people might consider that for example verbs are not important in a resume, so this can also be modified. In the function makeTable, the vriable parts_of_speech contains a list of the relevant parts of speech, according to the possible POS tags in NLTK (https://stackoverflow.com/questions/15388831/what-are-all-possible-pos-tags-of-nltk). The program will only consider phrases where all the words are in the parts_of_speech variable. For example, the phrase "Excellent communication skills" will be considered, since the three words are either adjectives or nouns, while the phrase "If you are" will not, because "if" is not a relevant POS. Additionally, there is a graylist variable, that will also remove words that are not relevant. For example, the word "you" in the job description context might not be relevant, and you might not want it to be considered. Simply add or remove POS tags in the parts_of_speech variable, or individual words in the graylist according to your preferences.
