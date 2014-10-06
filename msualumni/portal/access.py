from braces import views as access

class MSUAdminMixin(access.LoginRequiredMixin, access.UserPassesTestMixin):
	login_url = '/admin/login'
	redirect_field_name = 'next'

	def test_func(self, user):
		return user.is_staff