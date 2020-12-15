from django import forms


class AddForm(forms.Form):
    """Form for adding columns to ur schemas"""
    types = [
        ("date", "date"),
        ("integer", "integer"),
        ("phone", "phone"),
        ("email", "email"),
        ("name", "name"),
        ("address", "address"),
        ("domain", "domain"),
        ("job", "job"),
        ("company", "company"),
        ("text", "text"),
    ]
    Column_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    Type = forms.ChoiceField(choices=types, widget=forms.Select(attrs={"class": "form-control","id": "inputState"}))
    From = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}), required=False)
    To = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}), required=False)
    Sentences = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}), required=False)
    Order = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}))


class FullAddForm(forms.Form):
    """Form to add ur schema to DB"""
    Name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    Column_separator = forms.ChoiceField(choices=([("Comma (,)", "Comma (,)")]),
                                         widget=forms.Select(attrs={"class": "form-control","id": "inputState"}))
    String_character = forms.ChoiceField(choices=([('Double-quote (")', 'Double-quote (")')]),
                                         widget=forms.Select(attrs={"class": "form-control", "id": "inputState"}))


class RowForm(forms.Form):
    row = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}))
    num = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}))