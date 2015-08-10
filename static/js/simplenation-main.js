
$(document).ready(function(){

	var domain = "http://" + document.location.host;

	$('html').bind('click', function(event) {

    	currentElement = $('#'+event.target.id);
		if (!currentElement.hasClass("global-search-input"))
		{
			$('.suggestions').empty();
		}

		if (!currentElement.hasClass("search-tag-input"))
		{
			$('.tag-suggestions').empty();
		}

		if (!currentElement.hasClass("top"))
		{
			$('.term-sorting-button').removeClass("top");
		}

		if (!currentElement.hasClass("bottom"))
		{
			$('.term-sorting-button').removeClass("bottom");
		}

		if (!currentElement.hasClass("views"))
		{
			$('.term-sorting-button').removeClass("views");
		}

 	});

	

	var login_status_check = $('.login-status-check').attr("data-signal");
	var authenticated = false;
	if (login_status_check == "Y"){
		authenticated = true;
	}

	if (authenticated){
		are_new_notifications();
	}
	


	$('.email-confirmation-bar').on('click', '.send-email-confirmation', function(){
		var static_src = $('.static-src').attr("href");
		$('.send-email-confirmation').html('Sending...');
		send_email_confirmation();
		

	});

	$('.exp-body').each(function(){
		jQuery(this).linkify();
	});

    var dialog_opt = $( ".challenge-dialog" ).dialog({
	       	autoOpen: false,
     		modal: true,
     		width: 350,
     		position:['middle',120],
     		close: function(){
     			$("body").css('overflow','auto');
     		},
     		open: function(event,ui) {
     			$("body").css('overflow','hidden');
     			var dialogBlock = $(".ui-dialog");
     			var dialogHeadingBlock = $(".ui-dialog-titlebar");
     			var dialogHeadingSpan = $(".ui-dialog-title");
     			var dialogCloseButton = $(".ui-dialog-titlebar-close");
     			var dialogBody = $(".ui-dialog-content");
     			var dialogAuthorTitle = $(".dialog-author-title");


     			dialogBlock.css("padding","0").css("height", "350px");
     			dialogHeadingBlock.removeClass("ui-widget-header").css("border-radius","0px").css("background-color", "#e8e8e8");
     			dialogHeadingSpan.css("text-align", "left").css("color","#5c5c5c").css("font-size","18").css("font-weight","bold");
     			dialogCloseButton.css("background","#e8e8e8").css("border","1px solid #e8e8e8").css("outline","0");
     			dialogBody.css("height","90%").css("overflow-y","auto").css("overflow-x","hidden").css("padding","0px");
     			dialogAuthorTitle.css("color","#0091c2");

	            $('.ui-widget-overlay').bind('click', function(event,ui) {         
	                $('.challenge-dialog').dialog('close');
	            });
        	},
        	title: "Challenge favourites",
	});

	$( ".challenge-dialog-opener" ).click(function() {

		   var term_id = $(this).attr('data-termid');
	       dialog_opt.dialog( "open" );
	       challengee_list(term_id);
	       
	});

	$('.challenge-dialog').on('click','.dialog-challenge-button', function(){
		var challengee_id = $(this).attr('data-challengeeid');
		var term_id = $(this).attr('data-termid');

		if ($(this).hasClass("pressed")){
			$.growl({title:"Already challenged", message:"You have already challenged this person."});
		} else {
			
			challenge(challengee_id,term_id);
		}

	});
	
	var favorites_dialog_opt = $( ".favorites-list-dialog" ).dialog({
	       	autoOpen: false,
     		modal: true,
     		width: 350,
     		position:['middle',120],
     		close: function(){
     			$("body").css('overflow','auto');
     		},
     		open: function(event,ui) {
     			$("body").css('overflow','hidden');
     			var dialogBlock = $(".ui-dialog");
     			var dialogHeadingBlock = $(".ui-dialog-titlebar");
     			var dialogHeadingSpan = $(".ui-dialog-title");
     			var dialogCloseButton = $(".ui-dialog-titlebar-close");
     			var dialogBody = $(".ui-dialog-content");
     			var dialogAuthorTitle = $(".dialog-author-title");


     			dialogBlock.css("padding","0").css("height", "350px");
     			dialogHeadingBlock.removeClass("ui-widget-header").css("border-radius","0px").css("background-color", "#e8e8e8");
     			dialogHeadingSpan.css("text-align", "left").css("color","#5c5c5c").css("font-size","18").css("font-weight","bold");
     			dialogCloseButton.css("background","#e8e8e8").css("border","1px solid #e8e8e8").css("outline","0");
     			dialogBody.css("height","90%").css("overflow-y","auto").css("overflow-x","hidden").css("padding","0px");
     			dialogAuthorTitle.css("color","#0091c2");

	            $('.ui-widget-overlay').bind('click', function(event,ui) {         
	                $('.favorites-list-dialog').dialog('close');
	            });
        	},
        	title: "Favorite contributors",
	});

	$( ".favorite-number" ).click(function() {

	       favorites_dialog_opt.dialog( "open" );
	       
	});


	setInterval(function(){

		var login_status_check = $('.login-status-check').attr("data-signal");
		var authenticated = false;
		if (login_status_check == "Y"){
			authenticated = true;
		}
		if(authenticated)	
		{
			are_new_notifications();
		}
			

	}, 150000);



	$('.term-sorting-text').on('click', '.term-sorting-button', function(e){

		var currentElement = $(this);
		if (currentElement.hasClass("top")){
			currentElement.removeClass("top");
			currentElement.addClass("bottom");
			sortUsingNestedTextAscending($('.terms-filtered-container'), ".term-filtered", "div.term-stats-number.explanations");

		}
		else if(currentElement.hasClass("bottom")){
			currentElement.removeClass("bottom");
			currentElement.addClass("top");
			sortUsingNestedTextDescending($('.terms-filtered-container'), ".term-filtered", "div.term-stats-number.explanations");
		}
		else if(currentElement.hasClass("views")){
			sortUsingNestedTextDescending($('.terms-filtered-container'), ".term-filtered", "div.term-stats-number.term-views");
		}
		else {
			if(currentElement.text() == "posts"){
				currentElement.addClass("top");
				sortUsingNestedTextDescending($('.terms-filtered-container'), ".term-filtered", "div.term-stats-number.explanations");
			}
			else{
				currentElement.addClass("views");
				sortUsingNestedTextDescending($('.terms-filtered-container'), ".term-filtered", "div.term-stats-number.term-views");
			}
			
		}

	});



	//Global search on PRESS ENTER
	$('.global-search').on('keyup', '.global-search-input', function(e){
		e.stopPropagation();
		var inputElement = $(this);
		if (e.keyCode == 13) 
		{
			e.preventDefault();
    		return false;
		}
		else if (e.keyCode == 40)
		{
			
			var current_suggestion_number_string = $(".suggestions").find(".selected").attr('data-sugnumber');
			current_suggestion_number= parseInt(current_suggestion_number_string, 10)
			
			var next_suggestion_number = current_suggestion_number + 1;

			if (current_suggestion_number){
				if($("div[data-sugnumber='"+next_suggestion_number+"']").length){
					change_selection(current_suggestion_number, next_suggestion_number, inputElement);
				}
				else {
					next_suggestion_number = 0;
					change_selection(current_suggestion_number, next_suggestion_number, inputElement);
				}
			}
			else{
				current_suggestion_number = 0;
				next_suggestion_number = 0;
				change_selection(current_suggestion_number, next_suggestion_number, inputElement);

			}
			
			
			
		}
		else if (e.keyCode == 38){
			var current_suggestion_number_string = $(".suggestions").find(".selected").attr('data-sugnumber');
			current_suggestion_number= parseInt(current_suggestion_number_string, 10)
			
			var next_suggestion_number = current_suggestion_number - 1;
			if (current_suggestion_number){
				if($("div[data-sugnumber='"+next_suggestion_number+"']").length){
					change_selection(current_suggestion_number, next_suggestion_number, inputElement);
				}
				else {
					next_suggestion_number = 0;
					change_selection(current_suggestion_number, next_suggestion_number, inputElement);
				}
				
			}
			else{
				current_suggestion_number = 0;
				next_suggestion_number = 0;
				change_selection(current_suggestion_number, next_suggestion_number, inputElement);

			}
		}
		else {
			
			var search_item = $('.global-search-input').val();
			autocomplete_search(search_item);
			
		}
	});
			

	$('.tag-suggestions').on('click', '.tag-suggestion', function(){
			var search_tag_item = $(this).attr('data-tagname');
			tag_search(search_tag_item);
			$('#search-tag-input-id').val('');
			$('.tag-suggestions').empty();

	});

	$('.search-tags').on('click', '.search-tag-button', function(){
			var search_tag_item = $('#search-tag-input-id').val();
			tag_search(search_tag_item);
	});

	$('.search-tags').on('keyup', '.search-tag-input', function(e){
		
		var inputElement = $(this);

		if (e.keyCode == 13)
		{
			var search_tag_item = $('#search-tag-input-id').val();
			tag_search(search_tag_item);
			$('.tag-suggestions').empty();
			inputElement.val('');
		}
		else if (e.keyCode == 40)
		{
			
			var current_suggestion_number_string = $(".tag-suggestions").find(".selected").attr('data-sugnumber');
			current_suggestion_number= parseInt(current_suggestion_number_string, 10)
			
			var next_suggestion_number = current_suggestion_number + 1;

			if (current_suggestion_number){
				if($("div[data-sugnumber='"+next_suggestion_number+"']").length){
					change_selection(current_suggestion_number, next_suggestion_number, inputElement);
				}
				else {
					next_suggestion_number = 0;
					change_selection(current_suggestion_number, next_suggestion_number, inputElement);
				}
			}
			else{
				current_suggestion_number = 0;
				next_suggestion_number = 0;
				change_selection(current_suggestion_number, next_suggestion_number, inputElement);

			}
			
			
			
		}
		else if (e.keyCode == 38){
			var current_suggestion_number_string = $(".tag-suggestions").find(".selected").attr('data-sugnumber');
			current_suggestion_number= parseInt(current_suggestion_number_string, 10)
			
			var next_suggestion_number = current_suggestion_number - 1;
			if (current_suggestion_number){
				if($("div[data-sugnumber='"+next_suggestion_number+"']").length){
					change_selection(current_suggestion_number, next_suggestion_number, inputElement);
				}
				else {
					next_suggestion_number = 0;
					change_selection(current_suggestion_number, next_suggestion_number, inputElement);
				}
				
			}
			else{
				current_suggestion_number = 0;
				next_suggestion_number = 0;
				change_selection(current_suggestion_number, next_suggestion_number, inputElement);

			}
		}

		else {
			var search_item = $('.search-tag-input').val();
			autocomplete_tag_search(search_item);
		}
	});





	// Logic to handle tags on the index page
	$('.tag-choose-container').on('click', '.tag-choose', function(){
				
		var count = 0;
		var currently_pressed_tag = $(this).attr('data-tagname');
		var current_tag_id = $(this).attr('data-tagid');
		var tag_choose_list =  {};

		tag_choose_list = chosen_tags_list(currently_pressed_tag);
		count = Object.keys(tag_choose_list).length;
		
		if ($(this).css('background-color') == 'rgb(0, 145, 194)'){
			
			$(this).css('background-color','rgb(194, 194, 194)');
			$('#tag-unchoose-'+current_tag_id).css('background-color','rgb(194, 194, 194)');
		}else {
			
			$(this).css('background-color','rgb(0, 145, 194)');
			$('#tag-unchoose-'+current_tag_id).css('background-color','rgb(0, 145, 194)');
		}

		tag_filter(count, tag_choose_list);				
				
				
	});
	

	
	$('.tag-choose-container').on('click', '.tag-unchoose', function(){
	
		tag_name = $(this).attr('data-tagname');
		tag_id = $(this).attr('data-tagid');
		var obj = { 'tag_name':tag_name }
				$.ajax({
			           type: "POST",
			           url: domain + "/tag_deselect/",
			           contentType: 'application/json; charset=utf-8',
			           data: JSON.stringify(obj),
			           success: function(data) {
								$('#tag-filter-'+tag_id).remove();
								
			            },
			            error: function(rs, e) {
			                   alert(rs.responseText);
			            }
				});


	});
	
	

	// Login to handle tag addition/removal on the term page
	$('.tags-container-parent').on('click', '.tags-add', function(){
		
			
			var tagname = $('#tags-input-new').val();
			var termid = $(this).attr('data-termid');
			var signal = $(this).attr('data-signal');
			if (tagname){	
				$.ajax({
				           type: "GET",
				           url: domain + "/add_tags_to_term/",
				           data: { 'term_id': termid, 'tag_name': tagname, 'signal':signal}, //'csrfmiddlewaretoken': '{{csrf_token}}'},
				           success: function(data) {
									$('.tags-container').load(location.href + ' .tags-container');
				            },
				            error: function(rs, e) {
				                   alert(rs.responseText);
				            }
				});
			}


	});
	$('.tags-container-parent').on('keyup', '.tags-input', function(e){
		
		
		if (e.keyCode == 13)
		{
			
			$('.tags-add').click();
		}


	});

		
	$('.tags-container-parent').on('click', '.term-tag.delete',  function(){
		var tagname = $(this).attr('data-tagname');
		var termid = $(this).attr('data-termid');
		var signal = $(this).attr('data-signal');
		
		$.ajax({
		           type: "GET",
		           url: domain + "/add_tags_to_term/",
		           data: { 'term_id': termid, 'tag_name': tagname, 'signal':signal}, //'csrfmiddlewaretoken': '{{csrf_token}}'},
		           success: function(data) {
							$('.tags-container').load(location.href + ' .tags-container');
		            },
		            error: function(rs, e) {
		                   alert(rs.responseText);
		            }
		});

	});
		
	

	// Logic to handle favourites on the front end
	$('.favor-button').each(function(){
		$(this).click(function(){
			  
			  var favoree_id = $(this).attr('data-favoree-id');
			  var favor_button_text = $(this).text();

			  if (favor_button_text == "Add to favorites"){
			  	$(this).text("Added to favorites");
			  	$(this).addClass("is-favorite");
			  	add_favourites(favoree_id);
			  }
			  else {
			  	$(this).text("Add to favorites");
			  	$(this).removeClass("is-favorite");
			  	remove_favourites(favoree_id);
			  }
			 
				  
		});
	});

	$('.favorite-dialog-block').on('click','.dialog-add-favorite', function(){
		var to_favorite_id = $(this).attr("data-userid");
		var term_id = $(this).attr("data-termid");

		add_favourites_to_challenge(to_favorite_id, term_id);
		
		
	});



	
	$('.like-container').on('click', '.upvote', function(){

		var explanation_id = $(this).attr('data-expid');
		var signal = $(this).attr('data-signal');
		
		  if($(this).hasClass("upvoted")) {
		  	
			$('#likes-upvote-'+explanation_id).removeClass('upvoted');
			remove_like(explanation_id, signal);
		  } else if ($(this).hasClass("not-registered")){
		  	$.growl.warning({ title: "Please Log In", message: "You need to sign in to vote." });

		  } else {
		  	
			$('#likes-upvote-'+explanation_id).addClass('upvoted');
			$('#likes-downvote-'+explanation_id).removeClass('downvoted');
			add_like(explanation_id, signal);
		  }

	});

	$('.like-container').on('click', '.downvote', function(){

		var explanation_id = $(this).attr('data-expid');
		var signal = $(this).attr('data-signal');
		var likes_count = parseInt($('#likes-count-'+explanation_id).text(), 10);
		  if($(this).hasClass("downvoted")) {
		  	
			$('#likes-downvote-'+explanation_id).removeClass('downvoted');
			remove_like(explanation_id, signal);
		  } else if ($(this).hasClass("not-registered")){
		  	$.growl.warning({ title: "Please Log In", message: "You need to sign in to vote." });

		  } else {
		  	
			if (likes_count > 0){
				$('#likes-downvote-'+explanation_id).addClass('downvoted');
				$('#likes-upvote-'+explanation_id).removeClass('upvoted');
				add_like(explanation_id, signal);
			}
			else{
				$.growl.warning({message:'Vote count is already 0.'});
			}
		  }

	});

	// Logic to handle Report Inappropriate on the front end
	$('.reports_class').each(function(){
		$(this).click(function(){
			  
			  var expid = $(this).attr('data-expid');
			  var report_info = $(this).text();

			  $.ajax({
			           type: "GET",
			           url: domain + "/report_explanation/",
			           data: { 'explanation_id': $(this).attr('data-expid')}, //'csrfmiddlewaretoken': '{{csrf_token}}'},
			           success: function(data) {
								$('.report-container').html(data);
			                  
			            },
			            error: function(rs, e) {
			                   alert(rs.responseText);
			            }
          }); 
		});
	});



	// Logic to handle removal of pictures
	$('.pictures-container').on('click', '.remove-picture',  function(){
			var explanation_id = $(this).attr('data-expid');
			var picture_id = $(this).attr('data-pictureid');
			
			remove_picture(explanation_id, picture_id);
	});


	


	// Logic to handle addition of pictures
	$('.picture-add').each(function(){
			var explanation_id = $(this).attr('data-expid');
			$('#pictures-container-'+explanation_id).on('change', '#picture-of-'+explanation_id,  function(){
					
					var ext = $(this).val().split('.').pop().toLowerCase();
					if($.inArray(ext, ['png','jpg','jpeg']) == -1) {
						$.growl.warning({title:"Not a picture", message: "Please upload pictures with extensions jpg, jpeg or png."});
					}
					else{
						add_picture(explanation_id);
					}
					
					
			});
	});

	$('.pictures-container').on('click', '.add-picture', function(){
		var explanation_id = $(this).attr('data-expid');
		$('#picture-of-'+explanation_id).click();
	});


	$('.pictures-container').on('click', '.picture-thumbnail', function(){
		var explanation_id = $(this).attr('data-expid');
		var picture_id = $(this).attr('data-pictureid');
		$('.gallery-element-'+explanation_id).Am2_SimpleSlider();
		$('#gallery-element-'+picture_id).click();

	});
	


	$('.explanation-post-form').on( 'change', '.add-post-picture-input', function(){
			var preview_count = parseInt($(this).attr('data-count'), 10);
			var static_src = $('.static-src').attr("href");
			var ext = $(this).val().split('.').pop().toLowerCase();
			if($.inArray(ext, ['png','jpg','jpeg']) == -1) {
			    $.growl.warning({title:"Not a picture", message: "Please upload pictures with extensions jpg, jpeg or png."});
			}
			else{
				readURL(this, preview_count);
				$('#preview-picture-'+preview_count).show();
				$('#add-post-picture-wrapper-'+preview_count).hide();
				preview_count = preview_count + 1;
				$('.add-post-pictures').append('<div class="add-post-picture preview" id="preview-picture-'+preview_count+'" style="display:none; overflow:hidden;"><img class="add-post-picture-placeholder preview" id="add-post-picture-preview-'+ preview_count +'" data-count="'+ preview_count +'" src="#"><button class="remove-post-picture" id="remove-post-picture-'+ preview_count +'" data-count="'+ preview_count +'" type="button" style="border: 0px;">x</button></div>');
				$('.add-post-pictures').append('<div class="add-post-picture" id="add-post-picture-wrapper-'+ preview_count +'"><input class="add-post-picture-input" id="add-post-picture-'+ preview_count +'" data-count="'+preview_count+'" type="file" name="pictures" style="display:none;"><img class="add-post-picture-placeholder" id="add-post-picture-placeholder-'+ preview_count +'" data-count="'+ preview_count +'" src="'+ static_src+'images/add-photo@2x.png"></div>');
			}


	});

	$('.explanation-post-form').on('click', '.add-post-picture-placeholder', function(){
		var preview_count = parseInt($(this).attr('data-count'), 10);
		$('#add-post-picture-'+preview_count).click();
	});


	$('.explanation-post-form').on('click', '.remove-post-picture', function(){
		var preview_count = parseInt($(this).attr('data-count'), 10);
		$('#preview-picture-'+preview_count).remove();
		$('#add-post-picture-wrapper-'+preview_count).remove();
	});

	$('.explanation-post-form').on('click', '.post-button.not-registered', function(){

		$.growl.warning({ title: "Please Log In", message: "You need to sign in to POST." });
	});


	$('.edit-option-buttons').on('click', '.edit-button', function(){

		tinyMCE.triggerSave();
		var explanation_id = $(this).attr('data-expid');
		var body = $('#edit-input-'+ explanation_id).val();
		var signal = $(this).attr('data-signal');

		$.ajax({
			           type: "POST",
			           url: domain + "/edit_exp/",
			           data: { 'explanation_id': explanation_id, 'body':body,'signal': signal},
			           success: function(data) {
								location.reload();
			            },
			           error: function(rs, e) {
			                   alert("save button error reponse " + rs.responseText);
			            }
          		});

	});

	$('.edit-option-buttons').on('click', '.cancel-edit-button', function(){

		var explanation_id = $(this).attr('data-expid');

		cancel_edition(explanation_id);
		$('#edit-text-'+explanation_id).hide();
		$('#edit-option-'+explanation_id).hide();
		$('#add-picture-of-'+explanation_id).hide();

		
		$(".picture-container[data-expid='"+explanation_id+"']").each(function(){
				picture_id = $(this).attr('data-pictureid');
				$('#remove-picture-'+picture_id).hide();
		});
		
		$('#edit-'+explanation_id).show();
		$('#exp-body-'+ explanation_id).show();
		$('#see-more-'+ explanation_id).show();

	});

	$('.edit-option-buttons').on('click', '.delete-post-button', function(){

		var explanation_id = $(this).attr('data-expid');
		var signal = $(this).attr('data-signal');

				$.ajax({
			           type: "POST",
			           url: domain + "/edit_exp/",
			           data: { 'explanation_id': explanation_id, 'signal': signal},
			           success: function(data) {
								location.reload();
			            },
			            error: function(rs, e) {
			                   alert(rs.responseText);
			            }
          		});

	


	});

	$('.exp-container-parent').on('click', '.edit_class', function(){
		
		var explanation_id = $(this).attr('data-editid');

		$('#exp-body-'+ explanation_id).hide();
		$('#see-more-'+ explanation_id).hide();
		$('#edit-'+explanation_id).hide();
		$('#edit-text-'+explanation_id).show();
		$('#edit-option-'+explanation_id).show();
		$('#add-picture-of-'+explanation_id).show();

		$(".picture-container[data-expid='"+explanation_id+"']").each(function(){
				picture_id = $(this).attr('data-pictureid');
				$('#remove-picture-'+picture_id).show();
		});


	});


	$('.registration-form').on('change','.add-profile-picture', function(){

		var ext = $(this).val().split('.').pop().toLowerCase();
		if($.inArray(ext, ['png','jpg','jpeg']) == -1) {
			$.growl.warning({title:"Not a picture", message: "Please upload pictures with extensions jpg, jpeg or png."});
		}
		else{
			$('.profile-registration-mask').show();
			preview_profile_picture(this);
		}
		

	});

	$('.sign-post').on('click','.side-sign-option', function(){
		if (!$(this).hasClass("pressed")){
			if($(this).text() == 'sign up'){
				$('.in').removeClass("pressed");
				$('.up').addClass("pressed");
				$('#post-and-log-in-form').hide();
				$('#post-and-sign-up-form').show();
			}
			else{
				$('.up').removeClass("pressed");
				$('.in').addClass("pressed");
				$('#post-and-sign-up-form').hide();
				$('#post-and-log-in-form').show();
			}
		}
		
	});


 
});