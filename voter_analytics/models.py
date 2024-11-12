from django.db import models

# Create your models here.

class Voter(models.Model):
    '''
    Store/represent the data for voters in the town of Newton, MA
    last_name, first_name, st_no, st_name, apt_no, zip_code, dof_b, dof_reg
    party_aff, precinct_no, v20state, v21town, v21primary, v22general, v23town, voter_score
    '''
    last_name = models.TextField()
    first_name = models.TextField()
    st_no = models.IntegerField()
    st_name = models.TextField()
    apt_no = models.TextField()
    zip_code = models.IntegerField()
    dof_b = models.DateField() # date of birth
    dof_reg = models.DateField() # date of registration
    party_aff = models.TextField()
    precinct_no = models.IntegerField()
    v20state = models.TextField()
    v21town = models.TextField()
    v21primary = models.TextField()
    v22general = models.TextField()
    v23town = models.TextField()
    voter_score = models.IntegerField()

    def __str__(self):
        ''' Returns a string representation of this model instance
        '''
        return f'{self.first_name} {self.last_name} (Voter score: {self.voter_score})'
    
def load_data():
    ''' Function to load data records from CSV file into Django model instance
    '''
    # Delete all records before loading data to prevent deplication
    # Voter.objects.all().delete()

    filename = r"C:\Users\Computer\Desktop\Boston Univerity\Fall 2024\CS412 Full Stack Dev\newton_voters.csv"
    f = open(filename)
    headers = f.readline() # discard headers
    print(f'Headers: {headers}')
    l_no = 0
    for line in f:
        try:
            line = f.readline().strip()
            fields = line.split(',')
            # show which value in each field
            # for i in range(len(fields)):
            #     print(f'fields[{i}] = {fields[i]}')
            # create a new instance of a Voter object with this record from the CSV file
            voter = Voter(
                last_name=fields[1],
                first_name=fields[2],
                st_no=fields[3],
                st_name=fields[4],
                apt_no=fields[5],
                zip_code=fields[6],
                dof_b=fields[7],
                dof_reg=fields[8],
                party_aff=fields[9].strip(),
                precinct_no=fields[10],
                v20state=fields[11],
                v21town=fields[12],
                v21primary=fields[13],
                v22general=fields[14],
                v23town=fields[15],
                voter_score=fields[16]
            )
            voter.save()
            print(f'Loaded line {l_no}')
            l_no += 1
        except Exception as e:
            print(f'Exception {e} on {fields} at line {l_no}')
            l_no += 1
    print("Finished loading data")