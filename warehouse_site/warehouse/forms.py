from django import forms
from django.forms import HiddenInput
Name_Choices = (
    ('', 'Select Your name'),
    ('Alexander', 'Alexander'),
    ('Breanna', 'Breanna'),
    ('Dianne', 'Dianne'),
    ('Elizabeth', 'Elizabeth'),
    ('Emily', 'Emily'),
    ('Gary', 'Gary'),
    ('Jaden ', 'Jaden'),
    ('Jay', 'Jay'),
    ('Jenni', 'Jenni'),
    ('Jilian', 'Jilian'),
    ('Joshua', 'Joshua'),
    ('Kara', 'Kara'),
    ('Keisha', 'Keisha'),
    ('Kimberly ', 'Kimberly'),
    ('Kylie', 'Kylie'),
    ('LaDonna', 'LaDonna'),
    ('Lanny', 'Lanny'),
    ('Larisa', 'Larisa'),
    ('Liam', 'Liam'),
    ('Malachi', 'Malachi'),
    ('Mattison ', 'Mattison'),
    ('Mark', 'Mark'),
    ('Nathan', 'Nathan'),
    ('Oliver', 'Oliver'),
    ('Paul', 'Paul'),
    ('Renae', 'Renae'),
    ('Rhonda', 'Rhonda'),
    ('Shanon ', 'Shanon'),
    ('Shawn', 'Shawn'),
    ('Tami', 'Tami'),
    ('Tiffany', 'Tiffany'),
    ('Traci ', 'Traci'),
    ('Trent', 'Trent'),
    ('Troy', 'Troy :)'),
)

Store_num_Choices = (
    ('null', 'Choose a store number'),
    ('No Store Number', 'No Store Number '),
    ('100', '100'),
    ('101', '101'),
    ('103', '103'),
    ('108', '108'),
    ('110', '110'),
    ('118', '118'),
    ('119', '119'),
    ('123', '123'),
    ('131', '131'),
    ('202', '202'),
    ('204', '204'),
    ('205', '205'),
    ('206', '206'),
    ('211', '211'),
    ('212', '212'),
    ('214', '214'),
    ('220', '220'),
    ('222', '222'),
    ('224', '224'),
    ('BStock', 'BStock'),
    ('E - Commerce', 'E - Commerce'),
    ('Shared computer Refurb', 'Shared computer Refurb'),
)
storage_type_choices = (
    ('null', 'Choose Storage Type'),
    ('Tote', 'Tote'),
    ('Gaylord', 'Gaylord'),
    ('Other', 'Other'),

)

content_choice = (
    ('null', 'Choose Item Contents'),
    ('Computers', 'Computers'),
    ('Jewelry', 'Jewelry'),
    ('Collectables', 'Collectables'),
    ('Books', 'Books'),
    ('Media', 'Media'),
)
content_choice_books_media = (
    ('null', 'Choose Item Contents'),
    ('Books', 'Books'),
    ('Media', 'Media'),
)


class Userform(forms.Form):
    # user_name = forms.CharField(label='User name', max_length=100)
    user_name = forms.CharField(required=True, label='User name', widget=forms.TextInput(
        attrs={'class': "form-control", 'placeholder': 'User Name'}))
    password = forms.CharField(required=True, label='password', widget=forms.TextInput(
        attrs={'class': "form-control", 'placeholder': 'Password'}))


class TruckForm(forms.Form):
    Quant = forms.IntegerField(required=True, label='Quantity', widget=forms.TextInput(
        attrs={'class': "form-control", 'style': 'width: 50px'}))

    storage = forms.CharField(required=True, label='Item Container',
                              widget=forms.Select(choices=storage_type_choices,    attrs={'class': "form-control"}))

    store_number = forms.CharField(required=True, label='Store Number',
                                   widget=forms.Select(choices=Store_num_Choices,    attrs={'class': "form-control"}))

    item_contents = forms.CharField(required=True, label='Item Contentsr',
                                    widget=forms.Select(choices=content_choice,    attrs={'class': "form-control"}))
    problems = forms.CharField(required=False, label='Quantity', widget=forms.Textarea(
        attrs={'class': "form-control", 'style': 'width:200px;height:90px;resize:none;'}))


class ProcForm(forms.Form):
    hidden_sub = forms.CharField(disabled=True, widget=forms.TextInput(
        attrs={'class': "form-control", 'placeholder': 'Filters', 'style': 'width: 100px'}))
    store_number = forms.CharField(required=True, label='Store Number',
                                   widget=forms.Select(choices=Store_num_Choices,    attrs={'class': "form-control"}))
    storage = forms.CharField(required=True, label='Item Container',
                              widget=forms.Select(choices=storage_type_choices,    attrs={'class': "form-control"}))
    item_contents = forms.CharField(required=True, label='Item Contentsr',
                                    widget=forms.Select(choices=content_choice,    attrs={'class': "form-control"}))
    item_contents_books_media = forms.CharField(required=True, label='Item Contentsr',
                                                widget=forms.Select(choices=content_choice_books_media,    attrs={'class': "form-control"}))


class ProcDataForm(forms.Form):
    hidden_sub = forms.CharField(disabled=True, widget=forms.TextInput(
        attrs={'class': "form-control", 'placeholder': 'data', 'style': 'width: 100px'}))
    seal_num = forms.CharField(required=False, label='Seal Number', widget=forms.TextInput(
        attrs={'class': "form-control", 'placeholder': ''}))
    proc_by = forms.CharField(required=True, label='Processed By',
                              widget=forms.Select(choices=Name_Choices,    attrs={'class': "form-control", 'style': 'width:200px'}))
    man_number = forms.CharField(required=False, label='Manifest number', widget=forms.TextInput(
        attrs={'class': "form-control", 'placeholder': ''}))
    problems = forms.CharField(required=False, label='test', widget=forms.Textarea(
        attrs={'class': "form-control", 'style': 'width:200px;height:90px;resize:none;'}))
