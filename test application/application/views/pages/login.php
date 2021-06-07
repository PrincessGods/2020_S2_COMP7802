<section class="container mt-4">
	<legend class="border-bottom mb-4 mt-2"><h2 class="text-dark">Log In</h2></legend>
	<?php echo validation_errors(); ?>
	<?php echo form_open("includes/login_inc");

		if(isset($_COOKIE['u_id'])){
			echo '
				<div class="form-label-group">
					<label for="username">User name or Email</label>
					<input type="text" id="username" name="username" size="20" class="form-control" value="' .$_COOKIE['input_name']. '"/>
					<br>
				</div>

				<div class="form-label-group">
					<label for="password">Password</label>
					<input type="password" id="password" name="password" size="20" class="form-control" value="' .$_COOKIE['input_pwd']. '"/>
					<br>
				</div>
			';
		} else {
			echo '
				<div class="form-label-group">
					<label for="username">User name or Email</label>
					<input type="text" id="username" name="username" size="20" class="form-control"/>
					<br>
				</div>

				<div class="form-label-group">
					<label for="password">Password</label>
					<input type="password" id="password" name="password" size="20" class="form-control"/>
					<br>
				</div>
			';
		}
	?>
		<div class="checkbox mb-3">
			<label>
				<input name="reme" type="checkbox" value="remember-me"> Remember me
			</label>
		</div>

		<div class="form-label-group d-flex mt-2">
			<button class="btn btn-dark ml-auto text-light" type="submit" name="submit">Submit</button>
		</div>

	</form>

	<div class="border-top pt-3 mt-4">
		<small class="text-muted">
			Need An Account? <a class="ml-2 text-primary" href="signup">Sign Up Now</a>
		</small>
	</div>

</section>
