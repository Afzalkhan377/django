
from django.views.generic import ListView, DetailView
from .models import Voter
from django.shortcuts import render
from django.db.models import Q
from datetime import datetime
from django.views.generic import ListView
from .models import Voter

from django.db import models
class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100  

    def get_queryset(self):
        queryset = Voter.objects.all()

        # Get filter parameters from the request
        party_affiliation = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')

        # Filter by party affiliation if provided
        if party_affiliation:
            party_affiliation = party_affiliation.strip() 
            queryset = queryset.filter(party_affiliation=party_affiliation)

        # Filter by minimum date of birth if provided
        if min_dob:
            min_dob = f"{min_dob}-01-01"  
            min_dob = datetime.strptime(min_dob, '%Y-%m-%d').date()
            queryset = queryset.filter(date_of_birth__gte=min_dob)

        # Filter by maximum date of birth if provided
        if max_dob:
            max_dob = f"{max_dob}-12-31"  
            max_dob = datetime.strptime(max_dob, '%Y-%m-%d').date()
            queryset = queryset.filter(date_of_birth__lte=max_dob)

        # Filter by voter score if provided
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)

        # Filter by election participation if provided
        if self.request.GET.get('v20state'):
            queryset = queryset.filter(v20state=True)
        if self.request.GET.get('v21town'):
            queryset = queryset.filter(v21town=True)
        if self.request.GET.get('v21primary'):
            queryset = queryset.filter(v21primary=True)
        if self.request.GET.get('v22general'):
            queryset = queryset.filter(v22general=True)
        if self.request.GET.get('v23town'):
            queryset = queryset.filter(v23town=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add distinct party affiliations to the context
        context['party_affiliations'] = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        # Add a range of years to the context
        context['years'] = range(1900, datetime.now().year + 1)
        # Add distinct voter scores to the context
        context['voter_scores'] = Voter.objects.values_list('voter_score', flat=True).distinct()

        return context


class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

from django.views.generic import ListView
from .models import Voter
import plotly.express as px
import plotly.io as pio
from django.shortcuts import render

class GraphsView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        queryset = Voter.objects.all()

        # Get filter parameters from the request
        party_affiliation = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')

        # Filter by minimum date of birth if provided
        if min_dob:
            min_dob = f"{min_dob}-01-01"  
            min_dob = datetime.strptime(min_dob, '%Y-%m-%d').date()
            queryset = queryset.filter(date_of_birth__gte=min_dob)

        # Filter by maximum date of birth if provided
        if max_dob:
            max_dob = f"{max_dob}-12-31"  
            max_dob = datetime.strptime(max_dob, '%Y-%m-%d').date()
            queryset = queryset.filter(date_of_birth__lte=max_dob)

        # Filter by party affiliation if provided
        if party_affiliation:
            party_affiliation = party_affiliation.strip() 
            queryset = queryset.filter(party_affiliation=party_affiliation)

        # Filter by voter score if provided
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)

        # Filter by election participation if provided
        if self.request.GET.get('v20state'):
            queryset = queryset.filter(v20state=True)
        if self.request.GET.get('v21town'):
            queryset = queryset.filter(v21town=True)
        if self.request.GET.get('v21primary'):
            queryset = queryset.filter(v21primary=True)
        if self.request.GET.get('v22general'):
            queryset = queryset.filter(v22general=True)
        if self.request.GET.get('v23town'):
            queryset = queryset.filter(v23town=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the list of voters from the context
        quaryset = context['voters']

        # Create a histogram of birth years
        birth_years = [voter.date_of_birth.year for voter in quaryset]
        birth_year_fig = px.histogram(birth_years, nbins=20, labels={'value': 'Year of Birth'}, title="Voter Distribution by Birth Year")
        context['birth_year_graph'] = pio.to_html(birth_year_fig, full_html=False)

        # Create a pie chart of party affiliations
        party_counts = quaryset.values('party_affiliation').annotate(count=models.Count('party_affiliation'))
        party_data = {party['party_affiliation']: party['count'] for party in party_counts}
        party_fig = px.pie(names=list(party_data.keys()), values=list(party_data.values()), title="Voter Distribution by Party Affiliation")
        context['party_affiliation_graph'] = pio.to_html(party_fig, full_html=False)

        # Create a bar chart of election participation
        election_participation = {
            "2020 State": sum([voter.v20state for voter in quaryset]),
            "2021 Town": sum([voter.v21town for voter in quaryset]),
            "2021 Primary": sum([voter.v21primary for voter in quaryset]),
            "2022 General": sum([voter.v22general for voter in quaryset]),
            "2023 Town": sum([voter.v23town for voter in quaryset]),
        }
        election_participation_fig = px.bar(x=list(election_participation.keys()), y=list(election_participation.values()), title="Voter Participation in Elections", labels={'x': 'Election Year', 'y': 'Number of Voters'})
        context['election_participation_graph'] = pio.to_html(election_participation_fig, full_html=False)

        # Add distinct party affiliations to the context
        context['party_affiliations'] = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        # Add a range of years to the context
        context['years'] = range(1900, datetime.now().year + 1)
        # Add distinct voter scores to the context
        context['voter_scores'] = Voter.objects.values_list('voter_score', flat=True).distinct()

        return context
