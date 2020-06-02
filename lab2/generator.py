from faker import Faker
import random


class FileGenerator:
    file_name = 'generated.csv'

    first_names = ['Olga', 'Anna', 'Anton', 'Alex', 'George', 'Roman']
    last_names = ['Kuziv', 'Petrenko', 'Ivanenko', 'Snow', 'Cyrus']
    about_me = ['Some info', 'Hi people!', "It's a secret"]
    profile_links = ['http://twitter.com/', 'http://instagram.com/', 'http://facebook.com/']
    emails = ['@gmail.com', '@ukr.net', '@yahoo.com', '@yandex.ru']

    plan_titles = ['free', 'personal', 'premium', 'business', 'eCommerce']
    plan_prices = ['0', '4', '8', '25', '45']
    plan_descriptions = ['Month free trial', 'Best for personal use', 'Best for freelancers', 'Best for small businesses', 'Best for online stores']

    images = ['https://previews.123rf.com/images/derketta776/derketta7761908/derketta776190800077/127995966-ginger-cat-s-paw-on-the-blanket-selective-focus.jpg',
              'https://www.wallpaperup.com/uploads/wallpapers/2013/07/26/124262/528e158218788f6413b681af613d6f2f-700.jpg',
              'https://static.toiimg.com/photo/msid-68523832/68523832.jpg?1137762',
              'https://i.pinimg.com/736x/60/d9/26/60d9269a5ada1ee5e2f5161d036209e5.jpg',
              'https://static.boredpanda.com/blog/wp-content/uploads/2015/07/cutest-sleeping-kitties-ever-106__605.jpg']
    lorem_ipsum = ['Lorem ipsum dolor sit amet consectetur adipiscing elit. ', 'Ut in magna ac ex elementum placerat. ', 'Quisque molestie dui nec eleifend. ',
              'Vivamus aliquam odio id nibh bibendum vulputate. ', 'Aenean ut sem tincidunt gravida sapien varius porta neque. ', 'Integer a finibus enim ut blandit turpis. ',
              'Donec nec dapibus libero. ', 'Vivamus quis ipsum tortor. ', 'Sed ultrices risus vitae malesuada bibendum turpis elit aliquam ex facilisis. ']
    
    visibilities = ['public', 'private']
    allowing_comment = ['0', '1']

    records_count = 60


    def generate_purchase_plans(self, file):
        file.write('\nPurchasePlan\n')
        for i in range(0, len(self.plan_titles)):
            file.write('{plan_title},{plan_price},{plan_description}\n'
                        .format(plan_title=self.plan_titles[i], plan_price=self.plan_prices[i], plan_description=self.plan_descriptions[i]))


    def generate_users(self, file):
        file.write('\nUser\n')
        for i in range(self.records_count):
            first_name = self.first_names[random.randint(0, len(self.first_names) - 1)]
            last_name = self.last_names[random.randint(0, len(self.last_names) - 1)]
            public_display_name = first_name + last_name if random.randint(0, 1) else first_name + str(i)
            about_me = self.about_me[random.randint(0, len(self.about_me) - 1)] if random.randint(0, 1) else ''
            profile_link = self.profile_links[random.randint(0, len(self.profile_links) - 1)] + public_display_name if random.randint(0, 1) else ''
            email = public_display_name + self.emails[random.randint(0, len(self.emails) - 1)]
            password = random.randint(100000000, 999999999)

            file.write('{first_name},{last_name},{public_display_name},{about_me},{profile_link},{email},{password}\n'
                    .format(first_name=first_name, last_name=last_name, public_display_name=public_display_name,
                            about_me=about_me, profile_link=profile_link, email=email, password=password))


    def generate_following(self, file):
        file.write('\nFollow\n')
        for i in range(0, self.records_count):
            file.write('{id_follower},{id_following}\n'.format(id_follower=random.randint(1, self.records_count), id_following=random.randint(1, self.records_count)))


    def generate_purchase_settings(self, file):
        file.write('\nPurchaseSettings\n')
        for i in range(0, self.records_count):
            credit_card = random.randint(1000000000000000, 9999999999999999) if random.randint(0, 1) else ''
            id_plan = '1' if credit_card == '' else random.randint(2, len(self.plan_titles))
            file.write('{credit_card},{id_user},{id_plan}\n'.format(credit_card=credit_card, id_user=str(i+1), id_plan=id_plan))

    
    def generate_websites(self, file):
        file.write('\nWebsite\n')
        for i in range(0, self.records_count):
            title = self.lorem_ipsum[random.randint(0, len(self.lorem_ipsum) - 1)]
            file.write('{title},{id_author}\n'.format(title=title, id_author=random.randint(1, self.records_count)))

            
    def generate_content_blocks(self, file):
        file.write('\nContentBlock\n')
        for i in range(0, self.records_count):
            image = self.images[random.randint(0, len(self.images) - 1)]
            text = ''
            for i in range(0, len(self.lorem_ipsum) * 2):
                text += self.lorem_ipsum[random.randint(0, len(self.lorem_ipsum) - 1)]
            file.write('{image},{text},{id_website}\n'.format(image=image, text=text, id_website=random.randint(1, self.records_count)))


    def generate_site_settings(self, file):
        file.write('\nSiteSettings\n')
        for i in range(0, self.records_count):
            visibility = self.visibilities[random.randint(0, len(self.visibilities) - 1)]
            permalink = random.randint(10, 999999)
            allow_comment = self.allowing_comment[random.randint(0, len(self.allowing_comment) - 1)]
            file.write('{visibility},{permalink},{allow_comment},{id_website}\n'
                        .format(visibility=visibility, permalink=permalink, allow_comment=allow_comment, id_website=str(i+1)))

    def generate_comments(self, file):
        file.write('\nComment\n')
        fake = Faker()
        for i in range(0, self.records_count):
            body = self.lorem_ipsum[random.randint(0, len(self.lorem_ipsum) - 1)]
            timestamp = fake.date_between(start_date='-30d', end_date='now')
            file.write('{body},{timestamp},{id_author},{id_website}\n'.format(body=body, timestamp=timestamp,
                        id_author=random.randint(1, self.records_count), id_website=random.randint(1, self.records_count)))

    def generate_csv(self):
        with open(self.file_name, 'w') as file:
            self.generate_purchase_plans(file)
            self.generate_users(file)
            self.generate_following(file)
            self.generate_purchase_settings(file)
            self.generate_websites(file)
            self.generate_content_blocks(file)
            self.generate_site_settings(file)
            self.generate_comments(file)


if __name__ == '__main__':
    try:
        csv_generator = FileGenerator()
        csv_generator.generate_csv()
        print("File successfully generated")
    except:
        print("Error")