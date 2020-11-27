from django import forms

class ChallengesFilterForm(forms.Form):
    status1 = forms.BooleanField(required=False, label="Идет набор")
    status2 = forms.BooleanField(required=False, label="Активный")
    status3 = forms.BooleanField(required=False, label="Завершен")

    duration_max = forms.IntegerField(required=False, min_value=1)
    duration_min = forms.IntegerField(required=False, min_value=1)

    def is_form_empty(self):
        is_empty = cleaned_data['status1'] | cleaned_data['status2'] | cleaned_data['status3']
        is_empty = is_empty | (duration_max != None)
        is_empty = is_empty | (duration_min != None)

    def clean(self):
        cleaned_data = super(ChallengesFilterForm, self).clean()
        if (cleaned_data["duration_min"] != None) & (cleaned_data["duration_max"] != None):
            if cleaned_data["duration_min"] > cleaned_data["duration_max"]:
                raise forms.ValidationError("min > max")
