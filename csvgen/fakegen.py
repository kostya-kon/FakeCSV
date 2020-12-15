# there are fake generators
import random
import time
import string
from faker import Faker


def integer_gen(range_from, range_to):
    """Generate Integer field value"""
    return str(random.randint(range_from, range_to))


def date_gen():
    """Generate Date field value"""
    stime = time.mktime(time.strptime('1/1/2000', '%m/%d/%Y'))
    etime = time.mktime(time.strptime('1/1/2021', '%m/%d/%Y'))

    ptime = stime + random.random() * (etime - stime)

    return time.strftime('%m/%d/%Y', time.localtime(ptime))


def phone_gen():
    """Generate Phone number field value"""
    range_from = 10**(7-1)
    range_to = (10**7)-1
    return "(09" + str(random.randint(3, 9)) + ")" + str(random.randint(range_from, range_to))


def email_gen():
    """Generate Email field value"""
    extensions = ['com', 'net', 'org', 'gov']
    domains = ['gmail', 'yahoo', 'comcast', 'verizon',
               'charter', 'hotmail', 'outlook', 'frontier']

    extension = extensions[random.randint(0,len(extensions)-1)] # gen extension + domain
    domain = domains[random.randint(0,len(domains)-1)]

    account_len = random.randint(1,20) # gen account name
    account = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(account_len))

    finale = account + "@" + domain + "." + extension # combine
    return finale


# next only Faker`s gens


def name_gen():
    """Generate Full Name field value"""
    fake = Faker("en_US")
    return fake.name()


def address_gen():
    """Generate Address field value"""
    fake = Faker("en_US")
    return fake.address()


def domain_gen():
    """Generate Domain field value"""
    fake = Faker("en_US")
    return fake.domain_name()


def job_gen():
    """Generate Job field value"""
    fake = Faker("en_US")
    return fake.job()


def company_gen():
    """Generate Company name field value"""
    fake = Faker("en_US")
    return fake.bs()


def text_gen(n):
    """Generate Text field value (n = number of sentences)"""
    fake = Faker("en_US")
    return fake.paragraph(nb_sentences=n, variable_nb_sentences=False)