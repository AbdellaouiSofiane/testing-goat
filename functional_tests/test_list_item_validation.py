from selenium.webdriver.common.keys import Keys	
from unittest import skip
from .base import FunctionalTest




class ItemValidationTest(FunctionalTest):
	
	def test_cannot_add_empty_list_item(self):
		# Edith goes to the home page and accidentally tries to submit
		# an empty list item. She hits Enter on the empty input box
		self.browser.get(self.live_server_url)
		self.get_item_input_box().send_keys(Keys.ENTER)

		# The home page refreshes, and there is an error message saying
		# that list items cannot be blank
		self.wait_for(lambda: self.browser.find_elements_by_css_selector(
			'#id_text:invalid'
		))

		# She tries again with some text for the item, which now works
		self.get_item_input_box().send_keys('Buy milk')
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')

		# Perversely, she now decides to submit a second blank list item
		self.get_item_input_box().send_keys(Keys.ENTER)

		# She receives a similar warning on the list page
		self.wait_for(lambda: self.browser.find_elements_by_css_selector(
			'#id_text:invalid'
		))
		
		# And she can correct it by filling some text in
		self.get_item_input_box().send_keys('Make tea')
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for_row_in_list_table('2: Make tea')

	def test_cannot_duplicate_items_for_single_list(self):
		# Edith start a new list, she enters her first item
		self.browser.get(self.live_server_url)
		self.get_item_input_box().send_keys('do some stuff')
		self.get_item_input_box().send_keys(Keys.ENTER)

		# Item is shown in the table
		self.wait_for_row_in_list_table('1: do some stuff')

		# She forgets about that and tries to submit the same item
		# again
		self.get_item_input_box().send_keys('do some stuff')
		self.get_item_input_box().send_keys(Keys.ENTER)

		# She sees an error message telling her the item is already
		# in her list
		self.wait_for(lambda: self.assertEqual(
			self.browser.find_element_by_css_selector('.has-error').text,
			"You've already got this in your list"
		))
