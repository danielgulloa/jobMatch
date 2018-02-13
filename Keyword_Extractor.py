import re
import pandas as pd
import sys, os
import numpy as np
import nltk
import operator
import math

class Extractor():
	def __init__(self):
		self.softskills=self.load_skills('softskills.txt')
		self.hardskills=self.load_skills('hardskills.txt')
		self.jb_distribution=self.build_ngram_distribution(sys.argv[-2])
		self.cv_distribution=self.build_ngram_distribution(sys.argv[-1])
		self.table=[]
		self.outFile="Extracted_keywords.csv"

	def load_skills(self,filename):
		f=open(filename,'r')
		skills=[]
		for line in f:
			#removing punctuation and upper cases
			skills.append(self.clean_phrase(line)) 
		f.close()
		return list(set(skills))  #remove duplicates


	def build_ngram_distribution(self,filename):
		n_s=[1,2,3] #mono-, bi-, and tri-grams
		dist={}
		for n in n_s:
			dist.update(self.parse_file(filename,n))
		return dist
			

	def parse_file(self,filename,n):
		f=open(filename,'r')
		results={}
		for line in f:
			words=self.clean_phrase(line).split(" ")
			ngrams=self.ngrams(words,n)
			for tup in ngrams:
				phrase=" ".join(tup)
				if phrase in results.keys():
					results[phrase]+=1
				else:
					results[phrase]=1
		return results

	
	def clean_phrase(self,line):
		return re.sub(r'[^\w\s]','',line.replace('\n','').replace('\t','').lower())		
		


	def ngrams(self,input_list, n):
		return list(zip(*[input_list[i:] for i in range(n)]))

	def measure1(self,v1,v2):
		return v1-v2

	def measure2(self,v1,v2):
		return max(v1-v2,0)

	def measure3(self,v1,v2):#cosine similarity
		#"compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
    		sumxx, sumxy, sumyy = 0, 0, 0
    		for i in range(len(v1)):
        		x = v1[i]; y = v2[i]
        		sumxx += x*x
        		sumyy += y*y
        		sumxy += x*y
    		return sumxy/math.sqrt(sumxx*sumyy)


		

	def sendToFile(self):
		try:
    			os.remove(self.outFile)
		except OSError:
    			pass
		df=pd.DataFrame(self.table,columns=['type','skill','job','cv','m1','m2'])
		df_sorted=df.sort_values(by=['job','cv'], ascending=[False,False])
		df_sorted.to_csv(self.outFile, columns=['type','skill','job','cv'],index=False)

	def printMeasures(self):
		n_rows=len(self.table)		
		v1=[self.table[m1][4] for m1 in range(n_rows)]
		v2=[self.table[m2][5] for m2 in range(n_rows)]
		print("Measure 1: ",str(sum(v1)))
		print("Measure 2: ",str(sum(v2)))
		
		v1=[self.table[jb][2] for jb in range(n_rows)]
		v2=[self.table[cv][3] for cv in range(n_rows)]
		print("Measure 3 (cosine sim): ",str(self.measure3(v1,v2)))
			
		for type in ['hard','soft','general']:
			v1=[self.table[jb][2] for jb in range(n_rows) if self.table[jb][0]==type]
			v2=[self.table[cv][3] for cv in range(n_rows) if self.table[cv][0]==type]
			print("Cosine similarity for "+type+" skills: "+str(self.measure3(v1,v2)))		


	def makeTable(self):		
		#I am interested in verbs, nouns, adverbs, and adjectives
		parts_of_speech=['CD','JJ','JJR','JJS','MD','NN','NNS','NNP','NNPS','RB','RBR','RBS','VB','VBD','VBG','VBN','VBP','VBZ']
		graylist=["you", "will"]
		tmp_table=[]
		#look if the skills are mentioned in the job description and then in your cv
		
		for skill in self.hardskills:
			if skill in self.jb_distribution:
				count_jb=self.jb_distribution[skill]
				if skill in self.cv_distribution:
					count_cv=self.cv_distribution[skill]
				else:
					count_cv=0
				m1=self.measure1(count_jb,count_cv)
				m2=self.measure2(count_jb,count_cv)
				tmp_table.append(['hard',skill,count_jb,count_cv,m1,m2])

		for skill in self.softskills:
			if skill in self.jb_distribution:
				count_jb=self.jb_distribution[skill]
				if skill in self.cv_distribution:
					count_cv=self.cv_distribution[skill]
				else:
					count_cv=0
				m1=self.measure1(count_jb,count_cv)
				m2=self.measure2(count_jb,count_cv)
				tmp_table.append(['soft',skill,count_jb,count_cv,m1,m2])
						

		#And now for the general language of the job description:
		#Sort the distribution by the words most used in the job description

		general_language = sorted(self.jb_distribution.items(), key=operator.itemgetter(1),reverse=True)
		for tuple in general_language:
			skill = tuple[0]
			if skill in self.hardskills or skill in self.softskills or skill in graylist:
				continue
			count_jb = tuple[1]
			tokens=nltk.word_tokenize(skill)
			parts=nltk.pos_tag(tokens)
			if all([parts[i][1]in parts_of_speech for i in range(len(parts))]):
				if skill in self.cv_distribution:
					count_cv=self.cv_distribution[skill]
				else:
					count_cv=0
				m1=self.measure1(count_jb,count_cv)
				m2=self.measure2(count_jb,count_cv)
				tmp_table.append(['general',skill,count_jb,count_cv,m1,m2])
		self.table=tmp_table



def main():
	K=Extractor()
	K.makeTable()
	K.sendToFile()
	K.printMeasures()



if __name__ == "__main__":
    main()
		
