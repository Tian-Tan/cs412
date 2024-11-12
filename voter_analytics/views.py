from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
from django.db.models import Count

# Plotly packages
import plotly.express as px
import plotly.graph_objects as go

# Create your views here.
class VotersListView(ListView):
    ''' View to show a list of voters
    '''
    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        ''' Add the years list for date of birth to the context data
        '''
        context = super().get_context_data(**kwargs)
        context['years'] = list(range(1900, 2025))

        return context
    
    def get_queryset(self):
        ''' Apply logic for the filtering function
        '''
        queryset = super().get_queryset()

        party_affiliation = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')

        if party_affiliation:
            queryset = queryset.filter(party_aff=party_affiliation)
        if min_dob:
            queryset = queryset.filter(dof_b__year__gte=min_dob)
        if max_dob:
            queryset = queryset.filter(dof_b__year__lte=max_dob)
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)

        if self.request.GET.get('v20state') == 'yes':
            queryset = queryset.filter(v20state='TRUE')
        if self.request.GET.get('v21town') == 'yes':
            queryset = queryset.filter(v21town='TRUE')
        if self.request.GET.get('v21primary') == 'yes':
            queryset = queryset.filter(v21primary='TRUE')
        if self.request.GET.get('v22general') == 'yes':
            queryset = queryset.filter(v22general='TRUE')
        if self.request.GET.get('v23town') == 'yes':
            queryset = queryset.filter(v23town='TRUE')

        return queryset
    
class VoterDetailView(DetailView):
    ''' Display a single Voter on its own page
    '''
    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'v'
    
class GraphListView(ListView):
    ''' Display graphs using Plotly
    '''
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'v'

    def get_queryset(self):
        ''' Apply logic for the filtering function
        '''
        queryset = super().get_queryset()

        party_affiliation = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')

        if party_affiliation:
            queryset = queryset.filter(party_aff=party_affiliation)
        if min_dob:
            queryset = queryset.filter(dof_b__year__gte=min_dob)
        if max_dob:
            queryset = queryset.filter(dof_b__year__lte=max_dob)
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)

        if self.request.GET.get('v20state') == 'yes':
            queryset = queryset.filter(v20state='TRUE')
        if self.request.GET.get('v21town') == 'yes':
            queryset = queryset.filter(v21town='TRUE')
        if self.request.GET.get('v21primary') == 'yes':
            queryset = queryset.filter(v21primary='TRUE')
        if self.request.GET.get('v22general') == 'yes':
            queryset = queryset.filter(v22general='TRUE')
        if self.request.GET.get('v23town') == 'yes':
            queryset = queryset.filter(v23town='TRUE')

        return queryset
    
    def get_context_data(self, **kwargs):
        ''' Plot the graphs using Plotly
        '''
        # get the superclass version of context
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()

        # histogram for the distribution of voters by year of birth
        birth_years = [voter.dof_b for voter in voters]
        birth_year_hist = px.histogram(
            x=birth_years,
            title='Distribution of Voters by Year of Birth',
            labels={'x': 'Year of Birth', 'y': 'Count'},
        )
        birth_year_hist_div = birth_year_hist.to_html(full_html=False)

        # Create a pie chart for the distribution of voters by party affiliation
        party_counts = voters.values('party_aff').annotate(count=Count('id'))
        party_labels = [entry['party_aff'] for entry in party_counts]
        party_values = [entry['count'] for entry in party_counts]
        party_pie_chart = px.pie(
            names=party_labels,
            values=party_values,
            title='Distribution of Voters by Party Affiliation',
        )
        party_pie_chart_div = party_pie_chart.to_html(full_html=False)

        # histogram for voter participation in elections
        election_labels = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        election_counts = [
            voters.filter(**{label: "TRUE"}).count() for label in election_labels
        ]
        election_hist = go.Figure(
            data=[go.Bar(x=election_labels, y=election_counts)]
        )
        election_hist.update_layout(
            title='Voter Participation in Elections',
            xaxis_title='Election',
            yaxis_title='Count'
        )
        election_hist_div = election_hist.to_html(full_html=False)

        # add graphs to the context
        context['birth_year_hist_div'] = birth_year_hist_div
        context['party_pie_chart_div'] = party_pie_chart_div
        context['election_hist_div'] = election_hist_div

        return context