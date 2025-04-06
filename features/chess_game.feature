Feature: Play a game against the engine

  Scenario: Player chooses white and plays a legal move
    Given the game is initialized
    And the player chooses "white"
    When the player makes the move "e2e4"
    Then it should be black's turn
    And the engine should respond with a legal move
