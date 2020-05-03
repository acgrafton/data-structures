"""Functions to parse a file containing student data."""


def all_houses(filename):
    """Return a set of all house names in the given file.

    For example:
      >>> unique_houses('cohort_data.txt')
      {"Dumbledore's Army", 'Gryffindor', ..., 'Slytherin'}

    Arguments:
      - filename (str): the path to a data file

    Return:
      - set[str]: a set of strings
    """

    houses = set()

    cohort_data = open(filename)

    for line in cohort_data:
      house = line.strip().split("|")[2]
      if house:
        houses.add(house)

    cohort_data.close()

    return houses


def students_by_cohort(filename, cohort='All'):
    """Return a list of students' full names by cohort.

    Names are sorted in alphabetical order. If a cohort isn't
    given, return a list of all students. For example:
      >>> students_by_cohort('cohort_data.txt')
      ['Adrian Pucey', 'Alicia Spinnet', ..., 'Zacharias Smith']

      >>> students_by_cohort('cohort_data.txt', cohort='Fall 2015')
      ['Angelina Johnson', 'Cho Chang', ..., 'Terence Higgs', 'Theodore Nott']

      >>> students_by_cohort('cohort_data.txt', cohort='Winter 2016')
      ['Adrian Pucey', 'Andrew Kirke', ..., 'Roger Davies', 'Susan Bones']

      >>> students_by_cohort('cohort_data.txt', cohort='Spring 2016')
      ['Cormac McLaggen', 'Demelza Robins', ..., 'Zacharias Smith']

      >>> students_by_cohort('cohort_data.txt', cohort='Summer 2016')
      ['Alicia Spinnet', 'Dean Thomas', ..., 'Terry Boot', 'Vincent Crabbe']

    Arguments:
      - filename (str): the path to a data file
      - cohort (str): optional, the name of a cohort

    Return:
      - list[list]: a list of lists
    """

    students = []

    cohort_data = open(filename)

    for line in cohort_data:
      line = line.rstrip()
      student_profile_data = line.split("|")

      first_name, last_name, _, advisor, file_cohort = student_profile_data
      
      #Add student name to 'students' list if they are not an instructor or ghost.
      if cohort in ("All",file_cohort) and file_cohort not in ("I","G"):
        students = students + [(f"{first_name} {last_name}")]

    cohort_data.close()

    return sorted(students)


def all_names_by_house(filename):
    """Return a list that contains rosters for all houses, ghosts, instructors.

    Rosters appear in this order:
    - Dumbledore's Army
    - Gryffindor
    - Hufflepuff
    - Ravenclaw
    - Slytherin
    - Ghosts
    - Instructors

    Each roster is a list of names sorted in alphabetical order.

    For example:
      >>> rosters = hogwarts_by_house('cohort_data.txt')
      >>> len(rosters)
      7

      >>> rosters[0]
      ['Alicia Spinnet', ..., 'Theodore Nott']
      >>> rosters[-1]
      ['Filius Flitwick', ..., 'Severus Snape']

    Arguments:
      - filename (str): the path to a data file

    Return:
      - list[list]: a list of lists
    """

    dumbledores_army = []
    gryffindor = []
    hufflepuff = []
    ravenclaw = []
    slytherin = []
    ghosts = []
    instructors = []

    cohort_data = open(filename)

    for line in cohort_data:
        line = line.rstrip()
        student_profile_data = line.split("|")

        first_name, last_name, house, advisor, cohort = student_profile_data

        full_name = f"{first_name} {last_name}"

        if house == "Dumbledore's Army":
            dumbledores_army.append(full_name)

        elif house == "Gryffindor":
            gryffindor.append(full_name)

        elif house == "Hufflepuff":
            hufflepuff.append(full_name)

        elif house == "Ravenclaw":
            ravenclaw.append(full_name)

        elif house == "Slytherin":
            slytherin.append(full_name)

        elif cohort == "G":
            ghosts.append(full_name)

        elif cohort == "I":
            instructors.append(full_name)

    cohort_data.close()

    return [sorted(dumbledores_army),
            sorted(gryffindor),
            sorted(hufflepuff),
            sorted(ravenclaw),
            sorted(slytherin),
            sorted(ghosts),
            sorted(instructors)]


def all_data(filename):
    """Return all the data in a file.

    Each line in the file is a tuple of (full_name, house, advisor, cohort)

    Iterate over the data to create a big list of tuples that individually
    hold all the data for each person. (full_name, house, advisor, cohort)

    For example:
      >>> all_student_data('cohort_data.txt')
      [('Harry Potter', 'Gryffindor', 'McGonagall', 'Fall 2015'), ..., ]

    Arguments:
      - filename (str): the path to a data file

    Return:
      - list[tuple]: a list of tuples
    """

    all_data = []

    cohort_data = open(filename)

    for line in cohort_data:
        line = line.rstrip()
        student_profile_data = line.split("|")

        first_name, last_name, house, advisor, cohort = student_profile_data
        
        full_name = f"{first_name} {last_name}"
        
        all_data.append((full_name,house,advisor,cohort))

    cohort_data.close()       

    return all_data


def get_cohort_for(filename, name):
    """Given someone's name, return the cohort they belong to.

    Return None if the person doesn't exist. For example:
      >>> get_cohort_for('cohort_data.txt', 'Harry Potter')
      'Fall 2015'

      >>> get_cohort_for('cohort_data.txt', 'Hannah Abbott')
      'Winter 2016'

      >>> get_cohort_for('cohort_data.txt', 'Balloonicorn')
      None

    Arguments:
      - filename (str): the path to a data file
      - name (str): a person's full name

    Return:
      - str: the person's cohort or None
    """

    for full_name, _, _, cohort_name in all_data(filename):
      if name in full_name:
        return cohort_name


def find_duped_last_names(filename):
    """Return a set of duplicated last names that exist in the data.

    For example:
      >>> find_name_duplicates('cohort_data.txt')
      {'Creevey', 'Weasley', 'Patil'}

    Arguments:
      - filename (str): the path to a data file

    Return:
      - set[str]: a set of strings
    """

    cohort_data = open(filename)

    last_names = []

    for line in cohort_data:
        line = line.rstrip()
        student_profile_data = line.split("|")
        
        #Unpacking List with Identifiers
        first_name, last_name, house, advisor, cohort = student_profile_data

        #Create a list of all last names
        last_names = last_names + [last_name]

    #Loop through list of last names and add to set of duplicate last names    
    duplicate_last_names = {last_name for last_name in last_names
                          if last_names.count(last_name) > 1}

    return duplicate_last_names


def get_housemates_for(filename, name):
    """Return a set of housemates for the given student.

    Given a student's name, return a list of their housemates. Housemates are
    students who belong to the same house and were in the same cohort as the
    given student.

    For example:
    >>> get_housemates_for('cohort_data.txt', 'Hermione Granger')
    {'Angelina Johnson', ..., 'Seamus Finnigan'}
    """

    #Get student's cohort and assign variable.
    student_cohort = get_cohort_for(filename,name)

    #Get student's house and assign variable.
    for full_name, house, _, _ in all_data(filename):
      if name in full_name:
        student_house = house
        break

    #Create set with housemates.    
    housemates = {name 
                  for name, house, advisor, cohort in all_data(filename)
                  if student_house in house and name not in full_name}

    #Create set with all cohort_mates
    cohort_mates = {name 
                  for name, house, advisor, cohort in all_data(filename)
                  if student_cohort in cohort and name not in full_name}

    #Return intersection of housemates and cohort_mates
    return housemates & cohort_mates


##############################################################################
# END OF MAIN EXERCISE.  Yay!  You did it! You Rock!
#

if __name__ == '__main__':
    import doctest

    result = doctest.testfile('doctests.py',
                              report=False,
                              optionflags=(
                                  doctest.REPORT_ONLY_FIRST_FAILURE
                              ))
    doctest.master.summarize(1)
    if result.failed == 0:
        print('ALL TESTS PASSED')
