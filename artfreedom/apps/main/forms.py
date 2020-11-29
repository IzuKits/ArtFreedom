from django import forms

class ChallengesFilterForm(forms.Form):
    status1 = forms.BooleanField(required=False, label="Идет набор")
    status2 = forms.BooleanField(required=False, label="Активный")
    status3 = forms.BooleanField(required=False, label="Завершен")

    duration_max = forms.IntegerField(required=False, min_value=1)
    duration_min = forms.IntegerField(required=False, min_value=1)

    def is_form_empty(self):
        is_empty = self.cleaned_data['status1'] | self.cleaned_data['status2'] | self.cleaned_data['status3']
        is_empty = is_empty | (self.cleaned_data['duration_max'] != None)
        is_empty = is_empty | (self.cleaned_data['duration_min'] != None) 
    
    def is_status_filter_empty(self):
        return self.cleaned_data['status1'] | self.cleaned_data['status2'] | self.cleaned_data['status3']

    def is_duration_filter_empty(self):
        return (self.cleaned_data['duration_max']==None) & (self.cleaned_data['duration_min']==None)

    def clean(self):
        self.cleaned_data = super(ChallengesFilterForm, self).clean()
        if self.cleaned_data['duration_min'] == None:
            self.cleaned_data['duration_min'] = 0
        
        if (self.cleaned_data["duration_min"] != None) & (self.cleaned_data["duration_max"] != None):
            if self.cleaned_data["duration_min"] > self.cleaned_data["duration_max"]:
                raise forms.ValidationError("min > max")

    