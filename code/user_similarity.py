from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol


class UserSimilarity(MRJob):
	INPUT_PROTOCOL = JSONValueProtocol

	def extract_user_and_business(self, _, record):
		"""
		Given a review record, yields <user ID, business ID>.
		"""
		if record['type'] != 'review':
			return
		yield [record['user_id'], record['business_id']]

	def combine_businesses_by_user(self, user_ID, reviewed_business_IDs):
		"""
		Given a user and the businesses reviewed by the user,
		yields < _, (user, [businesses reviewed])>
		"""
		yield ['COMPUTE_JACCARD_COEFFICIENTS', (user_ID, list(reviewed_business_IDs))]

	def compute_jaccard_coefficient(self, set_1, set_2):
		"""
		Utility function that, given two sets, returns their Jaccard coefficient.
		"""
		set_1 = set(set_1)
		set_2 = set(set_2)
		intersection = set_1 & set_2
		union = set_1 | set_2
		return float(len(intersection)) / float(len(union))

	def compute_jaccard_coefficients(self, _, users_and_reviewed_businesses):
		"""
		Given values of the form (user, [businesses reviewed]),
		yields pairs of users and their respective reviews:
			<(user_1, user_2), ([businesses_1], [businesses_2])>
		The keys are (user_2, user_2) so that a Jaccard coefficient
		can be computed for each pair of users.
		"""
		users_and_reviewed_businesses = list(users_and_reviewed_businesses)
		for user_1, reviewed_businesses_1 in users_and_reviewed_businesses:
			for user_2, reviewed_businesses_2 in users_and_reviewed_businesses:
				if user_1 < user_2:
					jaccard_coefficient = self.compute_jaccard_coefficient(reviewed_businesses_1, reviewed_businesses_2)
					if jaccard_coefficient >= 0.5:
						yield [(user_1, user_2), jaccard_coefficient]
		
	def steps(self):
		"""
		Mapper 1:	<line, record> => <user ID, business ID>
		Reducer 1:	<user ID, [business IDs]> => <'constant', (user ID, [business IDs])>
		Mapper 2:	[identity function]
		Reducer 2:	<'constant', (user ID, [business IDs])> => <(user_1, user_2), Jaccard coefficient>
		"""
		return [
			self.mr(mapper=self.extract_user_and_business, reducer=self.combine_businesses_by_user),
			self.mr(reducer=self.compute_jaccard_coefficients),
		]


if __name__ == '__main__':
	UserSimilarity.run()
