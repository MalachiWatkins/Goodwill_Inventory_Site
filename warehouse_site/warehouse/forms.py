from django import forms

Name_Choices = (
    ('Currency', 'Currency'),
    ('Cards', 'Cards'),
    ('Accessories', 'Accessories'),
    ('Gems', 'Gems'),
    ('Jewels', 'Jewels'),
    ('Maps', 'Maps'),
    ('Weapons', 'Weapons'),
    ('Armour ', 'Armour'),
)

Store_num_Choices = (
    ('null', 'Choose a store number'),
    ('118', '118'),
    ('242', '242'),

)
storage_type_choices = (
    ('null', 'Choose Storage Type'),
    ('Tote', 'Tote'),
    ('Gaylord', 'Gaylord'),
    ('Other', 'Other'),

)

content_choice = (
    ('null', 'Choose Item Contents'),
    ('Jewelry', 'Jewelry'),
    ('Collectables', 'Collectables'),
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
    problems = forms.IntegerField(required=False, label='Quantity', widget=forms.Textarea(
        attrs={'class': "form-control", 'style': 'width:200px;height:90px;resize:none;'}))
