import psycopg2
from psycopg2 import Error
from dbconfig import dbconfig
from prompt import Prompt

class DBManager:

    p1 = Prompt()

    def Addt2i(self, p2):
        
        self.p1 = p2
        connection = None
        params = dbconfig()
        connection = psycopg2.connect(**params) # use all internal parameters from this dictionary
        cursor = connection.cursor()

        postgres_insert_query = """INSERT INTO tblt2i (positive, negative, sampler, steps, cfg, seed, size, modelhash, model, vaehash, clipskip, faceRestoration, adetailerModel, aDetailerPrompt, block) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        record_to_insert = (self.p1.positive, self.p1.negative, self.p1.sampler, self.p1.steps, self.p1.CFG, self.p1.seed, self.p1.size, self.p1.modelHash, self.p1.model, self.p1.vae, self.p1.clipSkip,self.p1.faceRestoration, self.p1.aDetailerModel, self.p1.aDetailerPrompt, self.p1.block)

        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into mobile table")

    def Addi2i(self, p2):
        
        self.p1 = p2
        connection = None
        params = dbconfig()
        connection = psycopg2.connect(**params) # use all internal parameters from this dictionary
        cursor = connection.cursor()

        postgres_insert_query = """INSERT INTO tbli2i (positive, negative, sampler, steps, cfg, seed, size, modelhash, model, vaehash, clipskip, denoisingStrength, faceRestoration, adetailerModel, aDetailerPrompt, block) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        record_to_insert = (self.p1.positive, self.p1.negative, self.p1.sampler, self.p1.steps, self.p1.CFG, self.p1.seed, self.p1.size, self.p1.modelHash, self.p1.model, self.p1.vae, self.p1.clipSkip, self.p1.denoiseStrength, self.p1.faceRestoration, self.p1.aDetailerModel, self.p1.aDetailerPrompt, self.p1.block)

        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into mobile table")

    def dbConnect(self):
        connection = None
        params = dbconfig()
        connection = psycopg2.connect(**params) # use all internal parameters from this dictionary
        cursor = connection.cursor()
        cursor.execute("select * from tblT2I")
        record = cursor.fetchall()

        for row in record:
            print("r:", row, "\n")   
