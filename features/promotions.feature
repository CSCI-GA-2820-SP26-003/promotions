Feature: The promotion store service back-end
    As a Promotion Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my promotions

Background:
    Given the following promotions
        | name                           | promotion_type | start_date | end_date   | value | active |
        | Free Shipping for New Members  | 1              | 2026-01-19 | 2026-02-18 | 10    | False  |
        | Spring Clearance               | 2              | 2026-03-01 | 2026-03-31 | 25    | True   |
        | VIP Bonus Discount             | 3              | 2026-04-01 | 2026-04-30 | 15    | True   |
        | Holiday Flash Sale             | 4              | 2026-12-01 | 2026-12-25 | 30    | False  |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Promotion Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a promotion
    When I visit the "Home Page"
    And I set the "Name" to "Welcome Discount"
    And I set the "Promotion Type" to "1"
    And I set the "Start Date" to "01-19-2026"
    And I set the "End Date" to "02-18-2026"
    And I set the "Value" to "10"
    And I select "False" in the "Active" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Promotion ID" field
    And I press the "Clear" button
    Then the "Promotion ID" field should be empty
    And the "Name" field should be empty
    And the "Promotion Type" field should be empty
    When I paste the "Promotion ID" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Welcome Discount" in the "Name" field
    And I should see "1" in the "Promotion Type" field
    And I should see "2026-01-19" in the "Start Date" field
    And I should see "2026-02-18" in the "End Date" field
    And I should see "10" in the "Value" field
    And I should see "False" in the "Active" dropdown

Scenario: List all promotions
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Free Shipping for New Members" in the results
    And I should see "Spring Clearance" in the results
    And I should see "VIP Bonus Discount" in the results
    And I should see "Holiday Flash Sale" in the results

Scenario: Search for active promotions
    When I visit the "Home Page"
    And I select "True" in the "Active" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Spring Clearance" in the results
    And I should see "VIP Bonus Discount" in the results
    And I should not see "Free Shipping for New Members" in the results
    And I should not see "Holiday Flash Sale" in the results

Scenario: Search for promotions by value
    When I visit the "Home Page"
    And I set the "Value" to "25"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Spring Clearance" in the results
    And I should not see "VIP Bonus Discount" in the results
    And I should not see "Holiday Flash Sale" in the results

Scenario: Update a promotion
    When I visit the "Home Page"
    And I set the "Name" to "Free Shipping for New Members"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Free Shipping for New Members" in the "Name" field
    And I should see "1" in the "Promotion Type" field
    When I change "Name" to "Free Shipping for VIP Members"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Promotion ID" field
    And I press the "Clear" button
    And I paste the "Promotion ID" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Free Shipping for VIP Members" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Free Shipping for VIP Members" in the results
    And I should not see "Free Shipping for New Members" in the results