$(document).ready(function(){
	
	are_new_notifications();

    var dialog_opt = $( ".challenge-dialog" ).dialog({
	       	autoOpen: false,
      		height: 300,
      		width: 350,
     		modal: true,     
	    });

	 $( ".challenge-dialog-opener" ).click(function() {
	       dialog_opt.dialog( "open" );
	 });


	function recent_notifications(){

			var obj = {}
			$.ajax({
			           type: "GET",
			           url: "/simplenation/recent_notifications/",
			           contentType: 'application/json; charset=utf-8',
			           data: JSON.stringify(obj),
			           success: function(data) {
								$('.notification-menu').html(data);
			            },
			            error: function(rs, e) {
			                   alert(rs.responseText);
			            }
			});
	}

	function are_new_notifications(){

			var obj = {}
			$.ajax({
			           type: "GET",
			           url: "/simplenation/are_new_notifications/",
			           contentType: 'application/json; charset=utf-8',
			           data: JSON.stringify(obj),
			           success: function(data) {
								if (data['notification_flag'] == true){
									$('.notification-indicator').text('('+data['num_of_unseen_notifications']+')')
								}
								else{
									;
								}
			            },
			            error: function(rs, e) {
			                   alert(rs.responseText);
			            }
			});

	}

	setInterval(function(){

			are_new_notifications();

	}, 30000);

	
	// $("body").click(function(e){
 //    	if(e.target.className !== "notification-menu")
 //    	{
 //      		$(".notification-menu").hide();
 //    	}
 //  	});


	// $('.notification-block').on('click', '.notification-button', function(){

	// 		recent_notifications();
	// 		$('.notification-menu').show('slow');
			

	// });


	function autocomplete_search(search_item){
			var obj = { 'search_item':search_item }
			$.ajax({
			           type: "POST",
			           url: "/simplenation/autocomplete_search/",
			           contentType: 'application/json; charset=utf-8',
			           data: JSON.stringify(obj),
			           success: function(data) {
								$('.suggestions').html(data);
			            },
			            error: function(rs, e) {
			                   alert(rs.responseText);
			            }
			});

	}


	//Global search on PRESS ENTER
	$('.global-search').on('keyup', '.global-search-input', function(e){
		if (e.keyCode == 13) 
		{
			e.preventDefault();
    		return false;
		}
		else {
			var search_item = $('.global-search-input').val();
			autocomplete_search(search_item);
		}
	});



	// Logic to handle TAG SEARCH on the front-end
	$('.search-tags').on('click', '.search-tag-button', function(){
		
			var search_tag_item = $('#search-tag-input-id').val();
			$.ajax({
			           type: "GET",
			           url: "/simplenation/search_tags/",
			           data: { 'search_tag_item': search_tag_item }, //'csrfmiddlewaretoken': '{{csrf_token}}'},
			           success: function(data) {
			           			if(data == 'No tags found, sorry'){
			           				$('#no-tags-message').html(data);
			           			}
			           			else {
			           				$('#no-tags-message').empty();
									$('.tag-choose-container').append(data);
									$('.tag-choose').each(function(){
										var count = 0
										var tagname_outer = $(this).attr('data-tagname');
										$('.tag-choose').each(function(){
											var tagname_inner = $(this).attr('data-tagname');
											if (tagname_outer == tagname_inner)
											{
												count = count + 1
												if(count > 1)
												{
													$('#tag-filter-'+$(this).attr('data-tagid')).remove();
													
												}
											}
										})
									});
								}
			            },
			            error: function(rs, e) {
			                   alert(rs.responseText);
			            }
			});


	});
	$('.search-tags').on('keyup', '.search-tag-input', function(e){
		
		
		if (e.keyCode == 13)
		{
			
			$('.search-tag-button').click();
		}


	});


		// Logic to handle tags on the index page
		$('.tag-choose').each(function(){
			$('.tag-choose-container').on('click', '#tag-choose-'+$(this).attr('data-tagid'), function(){
				
				var count = 0;
				var tagname_outer = $(this).attr('data-tagname');
				var tag_choose_list =  {};
				var duplicate_prevent_count = 0;

				$('.tag-choose').each(function(){
					if ($(this).css('font-weight') == 'bold') {
						if($(this).attr('data-tagname') != tagname_outer){

							count = count + 1;
							var tagname = $(this).attr('data-tagname');
							tag_choose_list['tag_name_' + count] = tagname;
						}
						else {
							;
						}


					} else {
						if($(this).attr('data-tagname') == tagname_outer){

							if(duplicate_prevent_count == 0){
								count = count + 1;
								var tagname = $(this).attr('data-tagname');
								tag_choose_list['tag_name_' + count] = tagname;
								duplicate_prevent_count = duplicate_prevent_count + 1;
							} else {
								;
							}

						}
					}
				});
				
				
				if ($(this).css('font-weight') == 'bold'){
					$(this).css('font-weight','normal');
				}else {
					$(this).css('font-weight','bold');
				}

				if(count == 0)
				{

				var obj = { 'number_of_tags':count }
				$.ajax({
			           type: "POST",
			           url: "/simplenation/tag_select/",
			           contentType: 'application/json; charset=utf-8',
			           data: JSON.stringify(obj),
			           success: function(data) {
								$('.container-tag-filtered-terms-index').html(data);
			            },
			            error: function(rs, e) {
			      
			                   alert(rs.responseText);
			            }
				});
				}
				else if (count > 0 && count<=5)
				{
				
				var obj = { 'number_of_tags':count, 'tag_choose_list': tag_choose_list }

				$.ajax({
			           type: "POST",
			           url: "/simplenation/tag_select/",
			           contentType: 'application/json; charset=utf-8',
			           data: JSON.stringify(obj),
			           success: function(data) {
								$('.container-tag-filtered-terms-index').html(data);
			            },
			            error: function(rs, e) {
			      
			                   alert(rs.responseText);
			            }
				});
				}
				
				
				
			});
		});

	$('.tag-unchoose').each(function(){
			$('.tag-choose-container').on('click', '#tag-unchoose-'+$(this).attr('data-tagid'), function(){
			
			$('#tag-choose-'+$(this).attr('data-tagid')).remove();
			$(this).remove();

			});
	});
	


	

	// Login to handle tag addition/removal on the term page
	$('.tags-container-parent').on('click', '.tags-add', function(){
		
			
			var tagname = $('#tags-input-new').val();
			var termid = $(this).attr('data-termid');
			var signal = $(this).attr('data-signal');

			$.ajax({
			           type: "GET",
			           url: "/simplenation/add_tags_to_term/",
			           data: { 'term_id': termid, 'tag_name': tagname, 'signal':signal}, //'csrfmiddlewaretoken': '{{csrf_token}}'},
			           success: function(data) {
								$('.tags-container').load(location.href + ' .tags-container');
			            },
			            error: function(rs, e) {
			                   alert(rs.responseText);
			            }
			});


	});
	$('.tags-container-parent').on('keyup', '.tags-input', function(e){
		
		
		if (e.keyCode == 13)
		{
			
			$('.tags-add').click();
		}


	});

	// setInterval(function(){
	// 	$('.tags-remove').each(function(){
	// 		$('.tags-container-parent').on('click', '#tags-remove-'+$(this).attr('data-tagid'),  function(){
	// 		var tagname = $(this).attr('data-tagname');
	// 		var termid = $(this).attr('data-termid');
	// 		var signal = $(this).attr('data-signal');
			
	// 		$.ajax({
	// 		           type: "GET",
	// 		           url: "/simplenation/add_tags_to_term/",
	// 		           data: { 'term_id': termid, 'tag_name': tagname, 'signal':signal}, //'csrfmiddlewaretoken': '{{csrf_token}}'},
	// 		           success: function(data) {
	// 							$('.tags-container').load(location.href + ' .tags-container');
	// 		            },
	// 		            error: function(rs, e) {
	// 		                   alert(rs.responseText);
	// 		            }
	// 		});

	// 		});
	// 	});
	// }, 900);


	function add_favourites(favoree_id)
	{
		var obj = { 'favoree_id': favoree_id}
		$.ajax({
			           type: "POST",
			           url: "/simplenation/add_favoree/",
			           contentType: 'application/json; charset=utf-8',
			           data: JSON.stringify(obj),
			           success: function(data) {
							   alert("Added to favourites.");   
			            },
			            error: function(rs, e) {
			                   alert(rs.responseText);
			            }
          });
	}

	function remove_favourites(favoree_id)
	{
		var obj = { 'favoree_id': favoree_id}
		$.ajax({
			           type: "POST",
			           url: "/simplenation/remove_favoree/",
			           contentType: 'application/json; charset=utf-8',
			           data: JSON.stringify(obj),
			           success: function(data) {
							   alert("Removed from favourites.");   
			            },
			            error: function(rs, e) {
			                   alert(rs.responseText);
			            }
          });
	}

	// Logic to handle favourites on the front end
	$('.favourites_class').each(function(){
		$(this).click(function(){
			  
			  var favoree_id = $(this).attr('data-favoree-id');
			  var favor_button_text = $(this).text();

			  if (favor_button_text == "Add to favourites"){
			  	$(this).text("Remove from favourites");
			  	add_favourites(favoree_id);
			  }
			  else {
			  	$(this).text("Add to favourites");
			  	remove_favourites(favoree_id);
			  }
			 
				  
		});
	});


	function add_like(explanation_id)
	{

		var obj={'explanation_id':explanation_id}

		jQuery.ajax({
			           type: "POST",
			           url: "/simplenation/add_like/",
			           contentType: 'application/json; charset=utf-8',
			           data: JSON.stringify(obj),
			           success: function(data) {
							   $('#likes-count-'+explanation_id).html(data+' <strong>likes</strong>');  
			            },
			            error: function(rs, e) {
			                   alert(rs.responseText);
			            }
          });

	}

	function remove_like(explanation_id)
	{
		var obj = {'explanation_id':explanation_id }

		jQuery.ajax({
			           type: "POST",
			           url: "/simplenation/remove_like/",
			           contentType: 'application/json; charset=utf-8',
			           data: JSON.stringify(obj),
			           success: function(data) {
							   $('#likes-count-'+explanation_id).html(data+' <strong>likes</strong>');  
			            },
			            error: function(rs, e) {
			                   alert(rs.responseText);
			            }
          });

	}

	// Logic to handle likes on the front end
	$('.likes_class').each(function(){
		$(this).click(function(){
			  
			  var explanation_id = $(this).attr('data-expid');
			  var like_info = $(this).text();

			  if(like_info == 'Like') {
				$('#likes-'+explanation_id).text('Unlike');
				add_like(explanation_id);
			  } else {
				$('#likes-'+explanation_id).text('Like');
				remove_like(explanation_id);
			  }

		});
	});

	// Logic to handle Report Inappropriate on the front end
	$('.reports_class').each(function(){
		$(this).click(function(){
			  
			  var expid = $(this).attr('data-expid');
			  var report_info = $(this).text();

			  $.ajax({
			           type: "GET",
			           url: "/simplenation/report_explanation/",
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


	// Logic to handle explanaiton edition/deletion on the front end	
	$('.edit_class').each(function(){
		var editid = $(this).attr('data-editid');
		$('#edit-'+editid).click(function(){
			
			
			
			if ($('#edit-form-'+editid).css('display') == 'none') {
				$('#edit-form-'+editid).show('slow');
				
			} else {
				$('#edit-form-'+editid).hide('slow');
				
			}
		});
		
			$('.edit-button').click(function(){
				tinyMCE.triggerSave();
				
				$.ajax({
			           type: "POST",
			           url: "/simplenation/edit_exp/",
			           data: { 'explanation_id': editid, 'body':$('#edit-input-'+editid).val(),'signal':$('#edit-input-'+editid).attr('data-signal')},
			           success: function(data) {
			           			//alert(data);
								$('#exp-container-'+editid).html(data);
			            },
			           error: function(rs, e) {
			                   alert(rs.responseText);
			            }
          		});

			});



			$('#delete-button-'+editid).click(function(){

				$.ajax({
			           type: "POST",
			           url: "/simplenation/edit_exp/",
			           data: { 'explanation_id': editid, 'signal':$(this).attr('data-signal')},
			           success: function(data) {
								location.reload();
			            },
			            error: function(rs, e) {
			                   alert(rs.responseText);
			            }
          		});

			});



		
	});
	
	// The following code handles csrf token retrieval
	// This function gets cookie with a given name
	function getCookie(name) {
	    var cookieValue = null;
	    if (document.cookie && document.cookie != '') {
	        var cookies = document.cookie.split(';');
	        for (var i = 0; i < cookies.length; i++) {
	            var cookie = jQuery.trim(cookies[i]);
	            // Does this cookie string begin with the name we want?
	            if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	}
	var csrftoken = getCookie('csrftoken');
	 
	/*
	The functions below will create a header with csrftoken
	*/
	 
	function csrfSafeMethod(method) {
	    // these HTTP methods do not require CSRF protection
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	function sameOrigin(url) {
	    // test that a given url is a same-origin URL
	    // url could be relative or scheme relative or absolute
	    var host = document.location.host; // host + port
	    var protocol = document.location.protocol;
	    var sr_origin = '//' + host;
	    var origin = protocol + sr_origin;
	    // Allow absolute or scheme relative URLs to same origin
	    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
	        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
	        // or any other URL that isn't scheme relative or absolute i.e relative.
	        !(/^(\/\/|http:|https:).*/.test(url));
	}
	 
	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
	            // Send the token to same-origin, relative URLs only.
	            // Send the token only if the method warrants CSRF protection
	            // Using the CSRFToken value acquired earlier
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    }
	});




});