# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pdb
from random import shuffle
from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout

from .models import Card, Member
from .forms import MemberForm, UpdateMemberForm
from django.conf import settings
from django.http import Http404, HttpResponse
from django.http import JsonResponse
from django.utils.safestring import mark_safe
import json
import random
import os


def home(request):
    return render(request, 'index.html')

@login_required
def index(request):
    if request.is_ajax():
        members = list(Member.objects.all().values('name', 'email', 'amount', 'photo'))
        return JsonResponse({'members': members})

    # for non-AJAX requests, render the index template as usual
    members = Member.objects.all()
    return render(request, 'index.html', {'members': members})

def logout_view(request):
    logout(request)
    return redirect('index')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('members')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('members')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def check_members(request):
    return render(request, 'members.html')


# @login_required
# def show_members(request):
#     members = Member.objects.filter(user=request.user)
#     return render(request, 'show_members.html', {'members': members})

@login_required
def show_members(request):
    members = Member.objects.all()
    return render(request, 'show_members.html', {'members': members, 'username': request.user.username})

@login_required
def add_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save(commit=False)
            member.user = request.user  # Set the default value for the user field
            member.save()
            return redirect('/members/')
    else:
        form = MemberForm()
    return render(request, 'add_member.html', {'form': form})

def update_member(request, pk):
    member = Member.objects.get(pk=pk)
    if member.user != request.user:
        return redirect('members')
    if request.method == 'POST':
        form = UpdateMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            return redirect('/members/')
    else:
        form = UpdateMemberForm(instance=member)
    return render(request, 'update_member.html', {'form': form})

def delete_member(request, pk):
    member = Member.objects.get(pk=pk)
    if member.user != request.user:
        return redirect('members')
    if request.method == 'POST':
        member.delete()
        return redirect('/members/')
    return render(request, 'delete_member.html', {'member': member})

#create function to show card image from card folder in /static/members and return the image
# def show_card_image(request, card):
#     card_path = os.path.join(settings.STATIC_ROOT, 'card_images', card + '.jpg')
#     if os.path.exists(card_path):
#         return render(request, 'card_images/' + card + '.jpg')
#     else:
#         raise Http404("Card does not exist")

def show_card_image(request, card_index):
    card_suit = card_index[-1]  # get the last character (suit) from the card index
    if card_suit == 'H':
        card_path = os.path.join(settings.STATIC_ROOT, 'card_images', f"{card_index}.jpg")
    elif card_suit == 'D':
        card_path = os.path.join(settings.STATIC_ROOT, 'card_images', f"{card_index}.jpg")
    elif card_suit == 'C':
        card_path = os.path.join(settings.STATIC_ROOT, 'card_images', f"{card_index}.jpg")
    elif card_suit == 'S':
        card_path = os.path.join(settings.STATIC_ROOT, 'card_images', f"{card_index}.jpg")
    else:
        raise Http404("Invalid card suit")
    print(card_path)  # add this line to print the path
    if os.path.exists(card_path):
        with open(card_path, 'rb') as f:
            return HttpResponse(f.read(), content_type='image/jpeg')
    else:
        raise Http404("Card does not exist")


# create cards for the deck and shuffle them and return 2 two cards to each player and 2 cards to the dealer
def deal_initial_cards(request):
    deck = [Card(suit, rank) for suit, rank in Card.PROPERTIES]
    random.shuffle(deck)
    
    dealer_cards = [deck.pop(), deck.pop()]
    player_cards = [[deck.pop(), deck.pop()] for _ in range(2)]
    
    return render(request, 'game.html', {'dealer_cards': dealer_cards, 'player_cards': player_cards})




# def game(request):
#     # Create a new deck of cards and shuffle it
#     deck = [Card(suit, rank) for suit, rank in Card.PROPERTIES()]
#     shuffle(deck)

#     # Deal initial cards
#     dealer_cards = [deck.pop(), deck.pop()]
#     player_cards = [deck.pop(), deck.pop()]

#     # Check if either the dealer or player has a natural blackjack
#     dealer_score = score(dealer_cards)
#     player_score = score(player_cards)
#     game_over = False
#     message = ""
#     game_state = ""

#     if player_score > 21:
#         message = "You went bust! Game over."
#         game_over = True
#     elif dealer_score > 21:
#         message = "Dealer went bust! You win!"
#         game_over = True
#     elif game_state == 'stand':
#         if dealer_score > player_score:
#             message = "Dealer wins!"
#             game_over = True
#         elif dealer_score == player_score:
#             message = "It's a tie!"
#             game_over = True
#         else:
#             message = "You win!"
#             game_over = True
#     else:
#         game_over = False
#         message = "Hit or stand?"

    # Pass the members context variable to the template
    members = Member.objects.all()
    context = {
        'dealer_cards': mark_safe(' '.join(map(str, dealer_cards))),
        'dealer_score': dealer_score,
        'player_cards': mark_safe(' '.join(map(str, player_cards))),
        'player_score': player_score,
        'game_over': game_over,
        'message': message,
        'members': members
    }

    return render(request, 'index.html', context)




def score(cards):
    """
    Calculate the score of a list of cards. Aces are worth 11 points unless
    the total score exceeds 21, in which case they are worth 1 point.
    """
    score = 0
    num_aces = 0
    for card in cards:
        value = card.get_value()
        score += value
        if value == 11:
            num_aces += 1
    while score > 21 and num_aces > 0:
        score -= 10
        num_aces -= 1
    return score


def add_card(request, member_id):
    # Add logic to append card to deck using member_id
    card_image_names = []  # empty list of image names
    card_images_json = json.dumps(card_image_names)
    deck_json = json.dumps([1, 2, 3, 4, 5])
    response_data = {
        'card_images_json': card_images_json,
        'deck_json': deck_json,
    }
    return JsonResponse(response_data)
   

def members(request):
    members = Member.objects.all()
    print(f"Number of members: {len(members)}")
    for member in members:
        print(f"Member name: {member.name}, email: {member.email}, amount: {member.amount}, photo: {member.photo.url}")
    
    return render(request, 'index.html', {'members': members})

    
