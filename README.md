- Has google oauth
- CSRF protection
- JWT based auth using HTTP only cookies
- Rate limiting
- Email based verification (token expires after some time)
- Uses beanie ODM
- Prevents usage of frequently used password during signup
- proper reset password email
- proper change password 
- proper forget password
- defined function for user based rate limiting
- session invalidation on password change
- admin panel

## More improvements

- [ ] Improve some redudancy in frontend code for api calls written twice and only one is used (auth context and individual auth frontend pages)
- [ ] Fix verification email functionality
- [ ] Fix google Oauth functionality
- [ ] Fix type errors in auth.py and get_user.py (intellisense)
- [ ] Replace email functionality with FastAPI
- [ ] Add fastAPI profiler to track performance
- [ ] implement forget password and change password while invalidating user session on password change  
