require 'minitest/autorun'
require_relative 'addition2'

class AdditionTest < Minitest::Test
  def test_1
    assert addition(1,2) == 3
  end