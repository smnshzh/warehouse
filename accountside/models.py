from django.db import models
from django.contrib.auth.models import User



class local_id_def(models.Model):

    city=models.CharField(max_length=12)
    local_name=models.CharField(max_length=12)
    local_code=models.PositiveSmallIntegerField()
    
    class Meta:
        ordering = ('city','local_code')

    def __str__(self):
        return f'{self.city}-{self.local_name}'

class kind(models.Model):

    type_code=models.PositiveIntegerField(verbose_name=('Code'))
    type_name= models.CharField(max_length=12,verbose_name=('Name'))
    def __str__(self):
        return self.type_name


class accountside(models.Model):

    slug=models.CharField(max_length=50)
    name= models.CharField(max_length=50)
    telephonnumber= models.CharField(max_length=11,unique=True)
    region=models.ForeignKey(local_id_def,on_delete=models.DO_NOTHING,blank=True,null=True)
    address=models.TextField(blank=True,null=True)
    credit=models.PositiveIntegerField(blank=True,null=True)
    property=models.BooleanField(default=False,blank=True,null=True)
    area=models.PositiveSmallIntegerField(blank=True,null=True)
    id_code=models.PositiveSmallIntegerField(unique=True,null=True)
    kind=models.ManyToManyField(kind)
    unique_together=['telephonnumber','id_code']


    def __str__(self):
        return self.name
    
class GeoAccount(models.Model):
    account = models.ForeignKey(accountside,on_delete=models.CASCADE)
    lat = models.FloatField ()
    long = models.FloatField ()



class AccountGroup(models.Model):
    code = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name

class TotalAccounts(models.Model):
    name = models.CharField(max_length=100)
    code = models.PositiveIntegerField(unique=True)
    account_group = models.ForeignKey(AccountGroup,on_delete=models.CASCADE)
    description = models.TextField (blank=True, null=True)

    class Meta:
        ordering = ("-code",)

    def __str__(self):
        return self.name

class DifinitAccounts(models.Model):


    name = models.CharField(max_length=100)
    code = models.PositiveIntegerField(unique=True)
    total_account = models.ForeignKey(TotalAccounts,on_delete=models.CASCADE)
    description = models.TextField (blank=True, null=True)
    def __str__(self):
        return self.name


class DocumentNumber(models.Model):

        code = models.PositiveIntegerField()
        creation_date = models.DateTimeField(auto_now_add=True)
        createur = models.ForeignKey(User,on_delete=models.DO_NOTHING)
        editable = models.BooleanField(default=False)


class Document(models.Model):

    number = models.ForeignKey(DocumentNumber,on_delete = models.CASCADE)
    difinit_account = models.ForeignKey(DifinitAccounts,on_delete = models.CASCADE )
    detailed_account = models.ForeignKey(accountside,on_delete = models.CASCADE,null=True,blank=True)
    debtor = models.DecimalField(max_digits=18,decimal_places=2,default=0)
    creditor = models.DecimalField(max_digits=18 , decimal_places=2,default=0)
    description = models.TextField()


class AutoJoournalFields (models.Model):


    name = models.CharField(max_length=45)
    credit_code = models.PositiveIntegerField()
    credit_code_2 = models.PositiveIntegerField (null=True,blank=True )
    credit_code_3 = models.PositiveIntegerField (null=True,blank=True )


    debt_code = models.PositiveIntegerField()
    debt_code_2 = models.PositiveIntegerField (null=True,blank=True )
    debt_code_3 = models.PositiveIntegerField ( null=True,blank=True)




    def __str__(self):

        return self.name



class BankCheck(models.Model):

    code = models.PositiveIntegerField(unique=True)
    slug = models.CharField (max_length=40)
    name = models.CharField(max_length=40)
    branch = models.CharField(max_length=40,blank=True,null=True)

    class Meta:
        unique_together = ("name", "branch")


class BankPose(models.Model):

    code = models.PositiveIntegerField (unique=True)
    slug = models.CharField (max_length=40)
    name = models.CharField (max_length=40)
    branch = models.CharField (max_length=40)
    accountside = models.ForeignKey(accountside,on_delete= models.CASCADE)

    class Meta:
        unique_together = ("name", "branch")

    def __str__(self):
        return f"{self.name} banck {self.branch}"

    def make_accountside(self):
        accountside.objects.create(
            slug=self.slug,
            name = self.name,
            kind = kind.objects.filter(type_code=4)
        )

    property(make_accountside)

class settel_kinde(models.Model):

    code = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=40)



class Safe_Box(models.Model):
    accountside = models.ForeignKey(accountside,on_delete=models.CASCADE)
    code = models.PositiveIntegerField()
    name = models.CharField(max_length=40)

    def __str__(self):

        return self.name


# class Setting(models.Model):
#
#     cheque_cash = models.PositiveIntegerField()
#        can_access_all_shipment = models.BooleanField()



