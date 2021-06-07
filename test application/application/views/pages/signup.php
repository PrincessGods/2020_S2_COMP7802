
<section class="container">
	<legend class="border-bottom mb-4 mt-5"><h2 class="text-dark">Join Today</h2></legend>
	<?php 
		$attr = array('class' => 'form-signin');
		echo form_open("includes/signup_inc", $attr); 
	?>
		<div class="form-label-group">
			<label for="username">User name</label>
			<input type="text" id ="username" name = "username" size = "20" class="form-control" />
			<br>
		</div>

		<div class="form-label-group">
			<label for="password">Password</label>
			<input type="password" id ="password" name = "password" size = "20" class="form-control" />
			<br>
		</div>

		<div class="form-label-group">
			<label for="email">Email</label>
			<input type="text" id ="email" name = "email" size = "20" class="form-control" />
			<br>
		</div>

		<div class="form-label-group">
			<label for="phone">Phone</label>
			<input type="text" id ="phone" name = "phone" size = "20" class="form-control" />
			<br>
		</div>

		<div class="form-label-group">
			<label for="country">Country</label>
			<input type="text" id ="country" name = "country" size = "20" class="form-control" />
			<br>
		</div>

		<div class="form-label-group">
			<label for="address">Address</label>
			<input type="text" id ="address" name = "address" size = "20" class="form-control" />
			<br>
		</div>

		<div class="form-label-group">
			<label for="exampleFormControlSelect1">Gender</label>
			<select class="form-control" id="selectSubject" name="gender">
				<option>Male</option>
				<option>Female</option>
				<option>Other</option>
			</select>
		<br>
		</div>

		<div class="form-label-group d-flex mt-2">
			<button class="btn btn-dark ml-auto text-light" type="submit" name="submit">Submit</button>
		</div>
	</form>

	<div class="border-top pt-3 mt-4 mb-5">
		<small class="text-muted">
			Already Have An Account? <a class="ml-2 text-primary" href="login">Sign In</a>
		</small>
	</div>
</section>
