## project/views.py
## define the views for the project

from django.shortcuts import render, get_object_or_404, redirect

# additional imports
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, View, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.urls import reverse
from plotly.express import pie, bar
from django.db.models import Count
import requests

# import other components
from .models import *
from .forms import *

# Create your views here.
class HomepageView(TemplateView):
    ''' A view to show a homepage template
    '''
    template_name = 'project/homepage.html'

    def get_context_data(self, **kwargs):
        ''' Add book count and user count to context data
        '''
        # Get the default context data
        context = super().get_context_data(**kwargs)

        # Add additional data for book count and user count
        context['book_count'] = Book.objects.count()
        context['user_count'] = User.objects.count()

        # Add the user's profile if the user is authenticated
        if self.request.user.is_authenticated:
            try:
                context['profile'] = Profile.objects.get(user=self.request.user)
            except Profile.DoesNotExist:
                context['profile'] = None
        else:
            context['profile'] = None

        return context

class ShowAllBooksView(ListView):
    ''' A view to show all Books currently available
    '''
    model = Book
    template_name = 'project/show_all_books.html'
    context_object_name = 'books'

class ShowAllProfilesView(ListView):
    ''' A view to show all Profiles
    '''
    model = Profile
    template_name = 'project/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowBookView(DetailView):
    ''' A view to show a single Book
    '''
    model = Book
    template_name = 'project/show_book.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        ''' Add context for borrowing status
        '''
        context = super().get_context_data(**kwargs)
        book = self.get_object()

        # Check if the book is currently borrowed
        context['is_borrowed'] = Borrow.objects.filter(book=book, returned_date__isnull=True).exists()
        return context

class ShowProfileView(DetailView):
    ''' A view to show a single Profile
    '''
    model = Profile
    template_name = 'project/show_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        ''' Add 'is_owner' to context, True if the logged-in user owns the profile. Also add borrowed_books to see all borrows of this user
        '''
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.request.user == self.get_object().user
        profile = self.get_object()
        borrowed_books = Borrow.objects.filter(profile=profile, returned_date__isnull=True)
        context['borrowed_books'] = borrowed_books
        context['past_borrows'] = Borrow.objects.filter(profile=profile, returned_date__isnull=False)
        return context

class SignUpProfileView(CreateView):
    ''' A view to allow for profile sign up
        GET: send back the form for display
        POST: process the form and save the new Profile to the database
    '''
    form_class = CreateProfileForm
    template_name = 'project/sign_up.html'

    def get_context_data(self, **kwargs):
        ''' Add built-in Django UserCreationForm to the context
        '''
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        ''' Django user creation, login user, and create profile
        '''
        # Reconstruct the UserCreationForm with POST data
        user_form = UserCreationForm(self.request.POST)
        
        # Check if both forms are valid
        if user_form.is_valid():
            # Save the User instance
            user = user_form.save()
            print(f'SignUpProfileView: created user {user}')
            # log the User in
            login(self.request, user)
            print(f'SignUpProfileView: {user} logged in')
            
            # Attach the User to the Profile instance before saving
            form.instance.user = user
            
            # Save the Profile and complete the process by calling superclass form_valid
            return super().form_valid(form)
        else:
            # If the user form is invalid, re-render the form with errors
            return self.form_invalid(form)
        
    def get_success_url(self):
        ''' Return the URL to redirect to on success
        '''
        return reverse('show_profile', kwargs={'pk':self.object.pk})
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    ''' A view to update a profile
    '''
    form_class = UpdateProfileForm
    template_name = "project/update_profile.html"
    model = Profile

    def get_success_url(self):
        ''' Return the URL to redirect to on success
        '''
        return reverse('show_profile', kwargs={'pk':self.object.pk})
    
    def get_login_url(self) -> str:
        ''' Return the URL of the login page
        '''
        return reverse('login')
    
    def get_object(self):
        ''' Return the Profile who called the update
        '''
        return get_object_or_404(Profile, user=self.request.user)
    
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    ''' View to show friend suggestions
    '''
    model = Profile # the model to display
    template_name = 'project/friend_suggestions.html'
    context_object_name = 'profile'

    def get_login_url(self) -> str:
        ''' Return the URL of the login page
        '''
        return reverse('login')
    
    def get_object(self):
        ''' Return the Profile who called the add Friend
        '''
        return get_object_or_404(Profile, user=self.request.user)
    
class CreateFriendView(LoginRequiredMixin, View):
    ''' A view to create a new Friend relation
    '''
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        other_pk = self.kwargs['other_pk']
        profile = Profile.objects.get(user=user)
        other_profile = Profile.objects.get(pk=other_pk)
        profile.add_friend(other_profile)

        return redirect(reverse('show_profile', kwargs={'pk':profile.pk}))
    
    def get_login_url(self) -> str:
        ''' Return the URL of the login page
        '''
        return reverse('login')
    
    def get_object(self):
        ''' Return the Profile who called the add Friend
        '''
        return get_object_or_404(Profile, user=self.request.user)
    
class CreateCommentView(LoginRequiredMixin, CreateView):
    ''' A view to create a Comment on a Book
    On GET: send back the form to display
    On POST: read/process the form, and save the new Comment to the database
    '''
    form_class = CreateCommentForm
    template_name = "project/create_comment.html"

    def get_context_data(self, **kwargs):
        ''' Creates a context dictionary and adds the Profile and Book objects to it
        '''
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, user=self.request.user)
        book = get_object_or_404(Book, pk=self.kwargs['pk'])  # `pk` from the URL corresponds to the Book
        context['profile'] = profile
        context['book'] = book
        return context

    def get_success_url(self):
        ''' Return the URL to redirect to on success
        '''
        return reverse('show_book', kwargs={'pk': self.kwargs['pk']})
    
    def get_login_url(self) -> str:
        ''' Return the URL of the login page
        '''
        return reverse('login')

    def form_valid(self, form):
        ''' This method is called after the form is validated, before saving data to the database
        '''
        print(f'CreateCommentView.form_valid() form={form.cleaned_data}')
        print(f'CreateCommentView.form_valid() self.kwargs={self.kwargs}')

        # Get the Profile of the logged-in user
        profile = get_object_or_404(Profile, user=self.request.user)

        # Get the Book object identified by the `pk` in the URL
        book = get_object_or_404(Book, pk=self.kwargs['pk'])

        # Associate the Comment instance with the Profile and Book
        form.instance.profile = profile
        form.instance.book = book

        # Delegate saving the form to the superclass method
        return super().form_valid(form)
    
class DeleteCommentView(LoginRequiredMixin, DeleteView):
    ''' A view to delete a comment
    '''
    model = Comment
    template_name = "project/delete_comment.html"
    context_object_name = "comment"

    def get_success_url(self):
        ''' Return the URL to redirect to after the delete
        '''
        # Get the pk for this comment
        pk = self.kwargs.get('pk')
        comment = Comment.objects.filter(pk=pk).first()  # Get one object from QuerySet

        # Find the book to which this comment is related by FK
        book = comment.book

        # Reverse to show the book page
        return reverse('show_book', kwargs={'pk': book.pk})

    def get_login_url(self):
        ''' Return the URL of the login page
        '''
        return reverse('login')
    
class UpdateCommentView(LoginRequiredMixin, UpdateView):
    ''' A view to update a comment
    '''
    form_class = UpdateCommentForm
    template_name = "project/update_comment.html"
    model = Comment
    context_object_name = "comment"

    def get_success_url(self):
        ''' Return the URL to redirect to after the update
        '''
        # Get the pk for this comment
        pk = self.kwargs.get('pk')
        comment = Comment.objects.filter(pk=pk).first()  # Get one object from QuerySet

        # Find the book to which this comment is related by FK
        book = comment.book

        # Reverse to show the book page
        return reverse('show_book', kwargs={'pk': book.pk})

    def get_login_url(self):
        ''' Return the URL of the login page
        '''
        return reverse('login')
    

class BorrowBookView(LoginRequiredMixin, View):
    ''' A view to handle borrowing a book
    '''

    def dispatch(self, request, *args, **kwargs):
        ''' Handles the borrow logic
        '''
        # Get the book object
        book = get_object_or_404(Book, pk=self.kwargs['pk'])

        # Check if the book is already borrowed and not returned
        if Borrow.objects.filter(book=book, returned_date__isnull=True).exists():
            # Redirect to the book detail page with an error message
            return redirect(f"{reverse('show_book', kwargs={'pk': book.pk})}?alert=already_borrowed")

        # If it's a POST request, handle the borrow logic
        if request.method == 'POST':
            # Get the profile of the logged-in user
            profile = get_object_or_404(Profile, user=request.user)

            # Create a new borrow record
            Borrow.objects.create(
                book=book,
                profile=profile,
                due_date=now() + timedelta(weeks=1)
            )

            # Redirect to the book detail page with a success message
            return redirect(f"{reverse('show_book', kwargs={'pk': book.pk})}?alert=success")

        # If it's not a POST request, redirect to the book detail page
        return redirect(reverse('show_book', kwargs={'pk': book.pk}))
    
    def get_login_url(self):
        ''' Return the URL of the login page
        '''
        return reverse('login')
    
class ReturnBookView(LoginRequiredMixin, View):
    ''' A view to return a borrowed book
    '''

    def dispatch(self, request, *args, **kwargs):
        ''' Handles the return logic
        '''
        # Get the borrow instance
        borrow = get_object_or_404(Borrow, pk=self.kwargs['pk'], profile__user=request.user)

        # Mark the book as returned
        borrow.returned_date = now()
        borrow.save()

        # Redirect to the user's profile page
        profile = get_object_or_404(Profile, user=self.request.user)
        return redirect('show_profile', pk=profile.pk)
    
    def get_login_url(self):
        ''' Return the URL of the login page
        '''
        return reverse('login')
    
class BorrowStatisticsView(ListView):
    ''' A view to display borrow statistics
    '''
    model = Borrow
    template_name = "project/borrow_statistics.html"
    context_object_name = "borrows"

    def get_context_data(self, **kwargs):
        ''' Add statistics and graphs to the context
        '''
        context = super().get_context_data(**kwargs)

        # Total borrows
        total_borrows = self.get_queryset().count()

        # Active and returned borrows
        active_borrows = self.get_queryset().filter(returned_date__isnull=True).count()
        returned_borrows = self.get_queryset().filter(returned_date__isnull=False).count()

        # Most borrowed books
        most_borrowed_books = (
            self.get_queryset()
            .values("book__title")
            .annotate(count=Count("id"))
            .order_by("-count")[:5]
        )

        # Pie chart for active vs returned borrows
        pie_chart_div = pie(
            names=["Active Borrows", "Returned Borrows"],
            values=[active_borrows, returned_borrows],
            title="Borrow Status Distribution",
        ).to_html(full_html=False)

        # Bar chart for most borrowed books
        bar_chart_div = bar(
            x=[entry["book__title"] for entry in most_borrowed_books],
            y=[entry["count"] for entry in most_borrowed_books],
            title="Top 5 Most Borrowed Books",
        ).to_html(full_html=False)

        # Add graphs to the context
        context['total_borrows'] = total_borrows
        context['active_borrows'] = active_borrows
        context['returned_borrows'] = returned_borrows
        context['pie_chart_div'] = pie_chart_div
        context['bar_chart_div'] = bar_chart_div

        return context
    
class BookQRView(DetailView):
    ''' A view to generate and display a QR code for a book
    '''
    model = Book
    template_name = "project/book_qr_code.html"
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        ''' Add qr code url that can be rendered to context
        '''
        context = super().get_context_data(**kwargs)

        # Get the book object
        book = self.get_object()

        # Generate the QR code URL using the qrserver API
        base_api_url = "https://api.qrserver.com/v1/create-qr-code/"
        qr_code_url = f"{base_api_url}?data={book.barcode_id}&size=200x200"

        # Add the QR code URL to the context
        context['qr_code_url'] = qr_code_url
        return context
    
class ScanQRCodeView(View):
    ''' A view to borrow a book by scanning its QR code
    '''

    def dispatch(self, request, *args, **kwargs):
        ''' Handle GET and POST requests '''
        if request.method == 'GET':
            # Render the QR code scanning page
            return render(request, "project/scan_qr_code.html")

        if request.method == 'POST':
            # Get the scanned QR code data
            scanned_uuid = request.POST.get("scanned_uuid")

            if not scanned_uuid:
                return render(request, "project/scan_qr_code.html", {
                    "error_message": "No QR code was scanned. Please try again."
                })

            # Find the book by its UUID
            book = get_object_or_404(Book, barcode_id=scanned_uuid)

            # Check if the book is already borrowed
            if Borrow.objects.filter(book=book, returned_date__isnull=True).exists():
                return render(request, "project/scan_qr_code.html", {
                    "error_message": f"The book '{book.title}' is already borrowed."
                })

            # Get the logged-in user's profile
            profile = get_object_or_404(Profile, user=request.user)

            # Create a borrow record
            Borrow.objects.create(
                book=book,
                profile=profile,
                due_date=now() + timedelta(weeks=1)
            )

            # Redirect to the book details page
            return redirect("show_book", pk=book.pk)