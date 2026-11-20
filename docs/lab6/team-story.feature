# Part D — Three Gherkin scenarios for our team story
# Team 22 · Cafeteria Pre-Order App
# Story PRECAFE-4: As a student, I can add items to a cart and change quantities,
#                  so that I can build my order.

Feature: Build an order in the cart
  As a student
  I want to add items to a cart and change quantities
  So that I can build my order

  Background:
    Given the menu has "Chicken wrap" for 45 EGP
    And the menu has "Orange juice" for 20 EGP
    And I am logged in as a student

  Scenario: Add an item to an empty cart
    Given my cart is empty
    When I add 1 "Chicken wrap" to my cart
    Then my cart shows 1 "Chicken wrap"
    And the cart total is 45 EGP

  Scenario: Change the quantity of an item
    Given my cart has 1 "Chicken wrap" and 1 "Orange juice"
    When I increase the quantity of "Orange juice" to 3
    Then my cart shows 3 "Orange juice"
    And the cart total is 105 EGP

  Scenario: A sold-out item cannot be added
    Given "Chicken wrap" is marked sold out
    When I try to add 1 "Chicken wrap" to my cart
    Then I see the message "Chicken wrap is sold out"
    And my cart is empty
