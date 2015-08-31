var domain = "http://" + document.location.host;
// Linkify: to convert all links within text to <a href=..></a>.
(function($){

		  var url1 = /(^|&lt;|\s)(www\..+?\..+?)(\s|&gt;|$)/g,
		      url2 = /(^|&lt;|\s)(((https?|ftp):\/\/|mailto:).+?)(\s|&gt;|$)/g,

		      linkifyThis = function () {
		        var childNodes = this.childNodes,
		            i = childNodes.length;
		        while(i--)
		        {
		          var n = childNodes[i];
		          if (n.nodeType == 3) {
		            var html = $.trim(n.nodeValue);
		            if (html)
		            {
		              html = html.replace(/&/g, '&amp;')
		                         .replace(/</g, '&lt;')
		                         .replace(/>/g, '&gt;')
		                         .replace(url1, '$1<a href="http://$2">$2</a>$3')
		                         .replace(url2, '$1<a href="$2">$2</a>$5');
		              $(n).after(html).remove();
		            }
		          }
		          else if (n.nodeType == 1  &&  !/^(a|button|textarea)$/i.test(n.tagName)) {
		            linkifyThis.call(n);
		          }
		        }
		      };

		  $.fn.linkify = function () {
		    return this.each(linkifyThis);
		  };

		})(jQuery);


// Challenge: to send request to server to challenge a user.
function challenge(challengee_id, term_id){
	$('#dialog-challenge-button-'+ challengee_id).addClass("button-bg-loader");
	var obj = {'challengee_id':challengee_id, 'term_id':term_id}
		$.ajax({
		           type: "POST",
		           url: domain + "/challenge/",
		           contentType: 'application/json; charset=utf-8',
		           data: JSON.stringify(obj),
		           success: function(data) {
		           		
	           			if(data['success']){
	           				$('#dialog-challenge-button-'+ challengee_id).removeClass("button-bg-loader");
	           				$.growl.notice({title:'Challenged', message:'You challenged <strong>'+data['challengee_name']+'</strong> to explain '+data['term_name']+'.'});
	           				$('#dialog-challenge-button-'+data['challengee_id']).addClass("pressed");
	          

	           			} else {
	           				$('#dialog-challenge-button-'+ challengee_id).removeClass("button-bg-loader");
	           				$.growl.warning({message: data['no_success_message']});
	           				$('#dialog-challenge-button-'+data['challengee_id']).addClass("pressed");

	           			}
				
		            },
		            error: function(rs, e) {
		                   console.log(rs.responseText);
		            }
		});
}


// Challengee List: Requests a list of challenged users for a term. Modifies the existing list in challenge dialog.
function challengee_list(term_id){
	var obj = { 'term_id':term_id }
	$.ajax({
		           type: "POST",
		           url: domain + "/challengee_list/",
		           contentType: 'application/json; charset=utf-8',
		           data: JSON.stringify(obj),
		           success: function(data) {
		           		
	           			if(data['challengee_list']){
	           				var challengee_list = data['challengee_list']
	           				for (i = 0; i < challengee_list.length; i++) { 
							    $('.dialog-challenge-button').each(function(){
							    	if($(this).attr('data-challengeeid')==challengee_list[i]['id']){
							    		
							    		$(this).addClass("pressed");
							    	}
							    });

							}


	           			}
				
		            },
		            error: function(rs, e) {
		                   console.log(rs.responseText);
		            }
		});

}



// Recent notifications: Requests last 20 notifications for a user. Modifies notification menu on response.
function recent_notifications(){

	var obj = {}
	$.ajax({
	           type: "GET",
	           url: domain + "/recent_notifications/",
	           contentType: 'application/json; charset=utf-8',
	           data: JSON.stringify(obj),
	           success: function(data) {
						$('.notification-menu').html(data);
	            },
	            error: function(rs, e) {
	                   console.log(rs.responseText);
	            }
	});
}


// Are new notifications: Polls the server for new notifications. Modifies the indicator on response.
function are_new_notifications(){

	var obj = {}
	$.ajax({
	           type: "GET",
	           url: domain + "/are_new_notifications/",
	           contentType: 'application/json; charset=utf-8',
	           data: JSON.stringify(obj),
	           success: function(data) {
						if (data['notification_flag']){
							$('.notifications-indicator').html(data['num_of_unseen_notifications'])
						}
	            },
	            error: function(rs, e) {
	                   console.log(rs.responseText);
	            }
	});

}


//Sort Ascending: Sorts the DOM elements based on their children
function sortUsingNestedTextAscending(parent, childSelector, keySelector) {
	var items = parent.children(childSelector).sort(function(a, b) {
	    var vA = $(keySelector, a).text();
	    var vB = $(keySelector, b).text();
	    var vA_int = parseInt(vA, 10);
	    var vB_int = parseInt(vB, 10);

	    return (vA_int < vB_int) ? -1 : (vA_int > vB_int) ? 1 : 0;
	});
	parent.append(items);
}


//Sort Descending: Sorts the DOM elements based on their children
function sortUsingNestedTextDescending(parent, childSelector, keySelector) {
	var items = parent.children(childSelector).sort(function(a, b) {
	var vA = $(keySelector, a).text();
	var vB = $(keySelector, b).text();
	var vA_int = parseInt(vA, 10);
	var vB_int = parseInt(vB, 10);

	return (vA_int > vB_int) ? -1 : (vA_int < vB_int) ? 1 : 0;
	});
	parent.append(items);
}



// Change Selection: moves focus from one DOM element in the list to another.
function change_selection(current_suggestion_number, next_suggestion_number, inputElement){

	var current_suggestion_element = $("div[data-sugnumber='"+current_suggestion_number+"']");
	var next_suggestion_element = $("div[data-sugnumber='"+next_suggestion_number+"']");

	if (next_suggestion_number != 0 && current_suggestion_number != 0){
		$("div[data-sugnumber='"+current_suggestion_number+"']").removeClass("selected");
		$("div[data-sugnumber='"+next_suggestion_number+"']").addClass("selected");
		if ($("div[data-sugnumber='"+next_suggestion_number+"']").children().text()){
			var text = $("div[data-sugnumber='"+next_suggestion_number+"']").children().text();
		}
		else{
			var text = $("div[data-sugnumber='"+next_suggestion_number+"']").text();
		}
		
		inputElement.val(text);

	}
	else if (current_suggestion_number != 0){
		if(current_suggestion_number == 1)
			{
				if ($("div[data-sugnumber='"+next_suggestion_number+"']").children().text()){
					var text = $("div[data-sugnumber='"+next_suggestion_number+"']").children().text();
				}
				else{
					var text = $("div[data-sugnumber='"+next_suggestion_number+"']").text();
				}
				inputElement.val(text);
				$("div[data-sugnumber='"+current_suggestion_number+"']").removeClass("selected");
			}
	}
	else {
		next_suggestion_number = 1;
		$("div[data-sugnumber='"+next_suggestion_number+"']").addClass("selected");
		if ($("div[data-sugnumber='"+next_suggestion_number+"']").children().text()){
			var text = $("div[data-sugnumber='"+next_suggestion_number+"']").children().text();
		}
		else{
			var text = $("div[data-sugnumber='"+next_suggestion_number+"']").text();
		}
		
		inputElement.val(text);
	}
}


// Autocomplete Search: Requests search suggestions for the input on the global search.
function autocomplete_search(search_item){
		var static_src = $('.static-src').attr("href");
		$('.global-search-form').append('<img class="global-search-loader" src="'+static_src+'images/loader.gif" width="15" height="15">');
		var obj = { 'search_item':search_item }
		$.ajax({
		           type: "POST",
		           url: domain + "/autocomplete_search/",
		           contentType: 'application/json; charset=utf-8',
		           data: JSON.stringify(obj),
		           success: function(data) {
		           			$('.global-search-loader').remove();
							$('.suggestions').html(data);
							var suggestion_number = 0;
							$('.suggestion').each(function(){
								suggestion_number = suggestion_number + 1;
								$(this).attr('data-sugnumber', function(){
									return suggestion_number;
								});
							});
		            },
		            error: function(rs, e) {
		            	   $('.global-search-loader').remove();
		                   console.log(rs.responseText);
		            }
		});

}
	

// Autocomplete Tag Search: Requests search suggestions for the input on the tag search.
function autocomplete_tag_search(search_item){
	var static_src = $('.static-src').attr("href");
	$('.search-tags-wrapper').append('<img class="tag-search-loader" src="'+static_src+'images/loader.gif" width="15" height="15">');
	var obj = { 'search_item':search_item }
	$.ajax({
	           type: "POST",
	           url: domain + "/autocomplete_tag_search/",
	           contentType: 'application/json; charset=utf-8',
	           data: JSON.stringify(obj),
	           success: function(data) {
	           			$('.tag-search-loader').remove();
	           			if (data != "not_found"){
							$('.tag-suggestions').html(data);
							var suggestion_number = 0;
							$('.tag-suggestion').each(function(){
								suggestion_number = suggestion_number + 1;
								$(this).attr('data-sugnumber', function(){
									return suggestion_number;
							});
						});
						}
						else{
							$('.tag-suggestions').empty();
						}
	            },
	            error: function(rs, e) {
	            	   $('.tag-search-loader').remove();
	                   console.log(rs.responseText);
	            }
	});

}


// Tag Search: Requests server to search for tags. Appends found tags to the tags block on the main page if found. 
function tag_search(search_tag_item){
		$.ajax({
		           type: "GET",
		           url: domain + "/search_tags/",
		           data: { 'search_tag_item': search_tag_item }, //'csrfmiddlewaretoken': '{{csrf_token}}'},
		           success: function(data) {
		           			if(data == 'No tags found, sorry'){
		           				$('.no-tags-message').show();
		           				setTimeout(function() {
    								$(".no-tags-message").fadeOut('slow');
								}, 1500);
		           			}
		           			else {
		           				$('.no-tags-message').hide();
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
									});
								});
							}

		            },
		            error: function(rs, e) {
		                   console.log(rs.responseText);
		            }
		});

}
	
// Chosen tags: Identifies the tags that are pressed, returns a list of pressed tags.
function chosen_tags_list(currently_pressed_tag){
		var tag_choose_list = {};
		var duplicate_prevent_count = 0;
		var count = 0;
		$('.tag-choose').each(function(){
				if ($(this).css('background-color') == 'rgb(0, 145, 194)') {
					if($(this).attr('data-tagname') != currently_pressed_tag){
						
						var tagname = $(this).attr('data-tagname');
						tag_choose_list['tag_name_' + count] = tagname;
						count = count + 1;
					}
					else {
						;
					}

				} 
				else {
					if($(this).attr('data-tagname') == currently_pressed_tag){

						if(duplicate_prevent_count == 0){
							
							var tagname = $(this).attr('data-tagname');
							tag_choose_list['tag_name_' + count] = tagname;
							count = count + 1;
							duplicate_prevent_count = duplicate_prevent_count + 1;
						} 
						else {
							;
						}

					}
				}
		});

		return tag_choose_list;

}
// Chosen tags: Identifies the tags that are pressed, returns a list of pressed tags.
function chosen_tags_list_no_args(){
		var tag_choose_list = {};
		var count = 0;
		if ($('.tag-choose').length){
			$('.tag-choose').each(function(){
				if ($(this).css('background-color') == 'rgb(0, 145, 194)') {
						var tagname = $(this).attr('data-tagname');
						tag_choose_list['tag_name_' + count] = tagname;
						count = count + 1;
				} 
			});
		}
		else if ($('.term-tag').length){
			var tagname = $('.term-tag.main').text();
			tag_choose_list['tag_name_' + count] = tagname;
			count = count + 1;
		}
		else {
			;
		}
		
		return tag_choose_list;

}

// Tag Filter: Sends a list of chosen tags to the server. Receives filtered terms and modifies main container.
// Note: filters up to infinite number of tags.
function tag_filter(count, tag_choose_list){
	var static_src = $('.static-src').attr("href");
	
	$('.terms-filtered-container').html('<img src="'+ static_src +'images/loader.gif" width="30" height="30">');	
			
	var obj = { 'number_of_tags':count, 'tag_choose_list': tag_choose_list }

	$.ajax({
           type: "POST",
           url: domain + "/tag_select/",
           contentType: 'application/json; charset=utf-8',
           data: JSON.stringify(obj),
           success: function(data) {
					$('.terms-filtered-container').html(data);
					isotopize();
            },
            error: function(rs, e) {
                   console.log(rs.responseText);
            }
	});
			

}

// Term sort: Sorts chosen container of elements.
// Note: filters up to infinite number of tags.
function universal_sort(count, tag_choose_list, sort_key, sort_direction){
	var static_src = $('.static-src').attr("href");
	
	$('.terms-filtered-container').html('<img src="'+ static_src +'images/loader.gif" width="30" height="30">');	
			
	var obj = { 'number_of_tags':count, 'tag_choose_list': tag_choose_list, 'sort_key':sort_key, 'sort_direction':sort_direction }

	$.ajax({
           type: "POST",
           url: domain + "/sort/",
           contentType: 'application/json; charset=utf-8',
           data: JSON.stringify(obj),
           success: function(data) {
					$('.terms-filtered-container').html(data);
					isotopize();
            },
            error: function(rs, e) {
                   console.log(rs.responseText);
            }
	});
			

}
	
function paginate(count, tag_choose_list, page_number, sort_key, sort_direction){
    var static_src = $('.static-src').attr("href");
	
	$('.terms-filtered-container').append('<img class="bottom-loader" src="'+ static_src +'images/loader.gif" width="30" height="30" style="margin-top:40px;margin-bottom:50px;">');		
	var obj = { 'number_of_tags':count, 'tag_choose_list': tag_choose_list , 'page_number':page_number, 'sort_key':sort_key, 'sort_direction':sort_direction};

	$.ajax({
           type: "POST",
           url: domain + "/paginate/",
           contentType: 'application/json; charset=utf-8',
           data: JSON.stringify(obj),
           success: function(data) {
           			$('.bottom-loader').remove();
           			if (data['success'] == false){
           				;
           			}
           			else {
						var page_number = $(data).filter(".page-numbers");
						$(".page-numbers").text(page_number.text());
						var $newItems = $(data);
						$('.grid').isotope( 'insert', $newItems );
           			}
					
            },
            error: function(rs, e) {
            		$('.bottom-loader').remove();
                   console.log(rs.responseText);
            }
	});

}

function get_page_number(){
	if ($('.page-numbers').length){
		return parseInt($('.page-numbers').text(),10);
	}
	else {
		return null;
	}
	
}
function get_total_pages(){
	if ($('.page-count').length){
		return parseInt($('.page-count').text(),10);
	}
	else{
		return null;
	}
}

function get_sort_key(){
	var sort_key = null;
	if($('.term-sorting-text').length){
		var postElement = $('#term-sorting-button-exp');
		var voteElement = $('#term-sorting-button-votes');
		var viewElement = $('#term-sorting-button-view');
		if (postElement.hasClass('top')||postElement.hasClass('bottom')){
			sort_key = postElement.text();
		}
		else if(voteElement.hasClass('ups')||voteElement.hasClass('downs')){
			sort_key = voteElement.text();
		}
		else if(viewElement.hasClass('views')){
			sort_key = viewElement.text();
		}
	}
	
	return sort_key;
	
}
function get_sort_direction(){
	var sort_direction = null;
	if($('.term-sorting-text').length){
		var postElement = $('#term-sorting-button-exp');
		var voteElement = $('#term-sorting-button-votes');
		var viewElement = $('#term-sorting-button-view');
		if (postElement.hasClass('top')||voteElement.hasClass('ups')||viewElement.hasClass('views')){
			sort_direction = "+";
		}
		else if(postElement.hasClass('bottom')||voteElement.hasClass('downs')){
			sort_key = "-";
		}
	}
	
	return sort_direction;
	
}
// Update Favorites List: Requests the server for updated favorite list. Modifies the list in DOM.	
function update_favoree_list(favoree_id, term_id){
	var obj = { 'term_id' : term_id}
	$.ajax({
		           type: "POST",
		           url: domain + "/update_favoree_list/",
		           contentType: 'application/json; charset=utf-8',
		           data: JSON.stringify(obj),
		           success: function(data) {
		           			
						  	$('.favorite-dialog-block').html(data);
						  	var dialogAuthorTitle = $(".dialog-author-title");
 							dialogAuthorTitle.css("color","#0091c2");
 							$('#dialog-add-favorite-'+ favoree_id).removeClass("button-bg-loader");
       						challengee_list(term_id);
		            },
		            error: function(rs, e) {
		                   console.log(rs.responseText);
		            }
      });
}


// Add Favorites: Sends a request to the server to add a new favorite. Modifies the challenge dialog block upon response
// by calling update_favoree_list
function add_favourites_to_challenge(favoree_id, term_id)
{
	$('#dialog-add-favorite-'+ favoree_id).addClass("button-bg-loader");
	var obj = { 'favoree_id': favoree_id}
	$.ajax({
		           type: "POST",
		           url: domain + "/add_favoree/",
		           contentType: 'application/json; charset=utf-8',
		           data: JSON.stringify(obj),
		           success: function(data) {
		           			if (data['success']){
		           				$.growl.notice({message:"Added to favourites."});
		           				update_favoree_list(favoree_id, term_id);  
		           			}
		           			else {
		           				$.growl.warning({message:data['no_success_message']});
		           				$('#dialog-add-favorite-'+ favoree_id).removeClass("button-bg-loader");
		           			}
						     
		            },
		            error: function(rs, e) {
		                   console.log(rs.responseText);
		            }
      });
}

// Add Favorites: Sends a request to the server to add a new favorite.
function add_favourites(favoree_id)
{
	var obj = { 'favoree_id': favoree_id}
	$.ajax({
		           type: "POST",
		           url: domain + "/add_favoree/",
		           contentType: 'application/json; charset=utf-8',
		           data: JSON.stringify(obj),
		           success: function(data) {
		           			if (data['success']){
		           				$.growl.notice({message:"Added to favourites."}); 
		           			}
		           			else {
		           				$.growl.warning({message:data['no_success_message']});
		           			}
						     
		            },
		            error: function(rs, e) {
		                   console.log(rs.responseText);
		            }
      });
}




// Remove Favorites: Sends a request to the server to remove a favorite.
function remove_favourites(favoree_id)
{
	var obj = { 'favoree_id': favoree_id}
	$.ajax({
		           type: "POST",
		           url: domain + "/remove_favoree/",
		           contentType: 'application/json; charset=utf-8',
		           data: JSON.stringify(obj),
		           success: function(data) {
		           			if (data['success']){
		           				$.growl({title:"Notice", message:"Removed from favourites."});     
		           			}
		           			else {
		           				$.growl.warning({message:data['no_success_message']});
		           			}
						  
		            },
		            error: function(rs, e) {
		                   console.log(rs.responseText);
		            }
      });
}


// Add like: Sends a request to add new like to a term
function add_term_like(term_id, signal)
{
	var static_src = $('.static-src').attr("href");
	if (signal == "up"){
		$('#likes-count-term-up-'+term_id).html('<img src="'+static_src+'images/loader.gif" width="10" height="10">');
	}
	else{
		$('#likes-count-term-down-'+term_id).html('<img src="'+static_src+'images/loader.gif" width="10" height="10">');
	}		
	var obj={'term_id':term_id, 'signal':signal}

	jQuery.ajax({
		           type: "POST",
		           url: domain + "/add_term_like/",
		           contentType: 'application/json; charset=utf-8',
		           data: JSON.stringify(obj),
		           success: function(data) {
		           		$('#likes-count-term-up-'+term_id).html(data['upvotes']);
						$('#likes-count-term-down-'+term_id).html(data['downvotes']);

		            },
		            error: function(rs, e) {
		                   console.log(rs.responseText);
		            }
      });

}

// Remove like: Sends a request to remove like from a term
function remove_term_like(term_id, signal)
{	
	var static_src = $('.static-src').attr("href");
	if (signal == "up"){
		$('#likes-count-term-up-'+term_id).html('<img src="'+static_src+'images/loader.gif" width="10" height="10">');
	}
	else{
		$('#likes-count-term-down-'+term_id).html('<img src="'+static_src+'images/loader.gif" width="10" height="10">');
	}
	
	
	var obj = {'term_id':term_id, 'signal':signal }

	jQuery.ajax({
		           type: "POST",
		           url: domain + "/remove_term_like/",
		           contentType: 'application/json; charset=utf-8',
		           data: JSON.stringify(obj),
		           success: function(data) {
							$('#likes-count-term-up-'+term_id).html(data['upvotes']);
							$('#likes-count-term-down-'+term_id).html(data['downvotes']);
						
		            },
		            error: function(rs, e) {
		                   console.log(rs.responseText);
		            }
      });

}

// Add like: Sends a request to add new like to an explanation
function add_like(explanation_id, signal)
{

	var obj={'explanation_id':explanation_id, 'signal':signal}

	jQuery.ajax({
		           type: "POST",
		           url: domain + "/add_like/",
		           contentType: 'application/json; charset=utf-8',
		           data: JSON.stringify(obj),
		           success: function(data) {
						   $('#likes-count-'+explanation_id).html(data);  
		            },
		            error: function(rs, e) {
		                   console.log(rs.responseText);
		            }
      });

}


// Remove like: Sends a request to remove like from an explanation
function remove_like(explanation_id, signal)
{
	var obj = {'explanation_id':explanation_id, 'signal':signal }

	jQuery.ajax({
		           type: "POST",
		           url: domain + "/remove_like/",
		           contentType: 'application/json; charset=utf-8',
		           data: JSON.stringify(obj),
		           success: function(data) {
						   $('#likes-count-'+explanation_id).html(data);  
		            },
		            error: function(rs, e) {
		                   console.log(rs.responseText);
		            }
      });

}

	
// Cancel Edition: Requests a server to remove preloaded images within the explanation.
function cancel_edition(explanation_id){
	var obj = {'explanation_id':explanation_id }

	jQuery.ajax({
       type: "POST",
       url: domain + "/cancel_edition/",
       contentType: 'application/json; charset=utf-8',
       data: JSON.stringify(obj),
       success: function(data) {
			   $('#pictures-container-'+explanation_id).html(data);
       },
       error: function(rs, e) {
               console.log(rs.responseText);
       }
      });

}

// Add a picture: Preloads an image to the server. Modifies DOM upon response.
function add_picture(explanation_id){
	var data = new FormData($('#picture-form-'+explanation_id).get(0));
	var static_src = $('.static-src').attr("href");

	$('#add-picture-of-'+ explanation_id).empty();
	$('#add-picture-of-'+ explanation_id).addClass("loader");

	$.ajax({
		url: $('#picture-form-'+explanation_id).attr('action'),
		type: $('#picture-form-'+explanation_id).attr('method'),
		data: data,
		cache: false,
		processData: false,
		contentType: false,
		success: function(data) {
			if(data['no_success_message']){
       		   	$.growl.warning({title:"Not a picture", message: "Please upload pictures, e.g. jpeg, png etc."});
       		   	$('#add-picture-of-'+ explanation_id).removeClass("loader");
       		   	$('#add-picture-of-'+ explanation_id).append('<img class="add-picture-placeholder" src="'+ static_src +'images/add-photo@2x.png">');
       		}
       		else {
				$('#add-picture-of-'+explanation_id).remove();
				$('#picture-edit-'+ explanation_id).remove();
    			$('#pictures-container-'+explanation_id).append(data);
    		}
		},
		error: function(rs, e) {
		    console.log(rs.responseText);
		}
	});

}


// Remove a picture: Sends a request to remove a picture from an explanation
function remove_picture(explanation_id, picture_id){
	var obj = {'picture_id':picture_id }

	jQuery.ajax({
       type: "POST",
       url: domain + "/remove_picture/",
       contentType: 'application/json; charset=utf-8',
       data: JSON.stringify(obj),
       success: function(data) {
       		   
		   		$('#picture-container-'+picture_id).remove();
		  		$('#gallery-element-'+picture_id).remove();
       		   
       		   
       },
       error: function(rs, e) {
               console.log(rs.responseText);
       }
      });

	

}


	
// Preview a picture by changing src attribute
function readURL(input, preview_count) {
	
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        
        reader.onload = function (e) {
  
            $('#add-post-picture-preview-'+preview_count).attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}
	


	
// Preview a profile picture by changing src attribute
function preview_profile_picture(input) {

    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
        	
            $('.profile-registration-img').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}

// Preview a default picture by changing src attribute
function preview_default_picture(input) {
	var static_src = $('.static-src').attr("href");
    $('.profile-registration-img').attr('src', static_src+'images/imageholder.png');
}


function send_email_confirmation(){
	var obj = {}

	jQuery.ajax({
       type: "POST",
       url: domain + "/send_email_confirmation/",
       contentType: 'application/json; charset=utf-8',
       data: JSON.stringify(obj),
       success: function(data) {
       		   if(data['success']){
					$.growl.notice({title:"Email sent", message:"Confirmation email has been sent."});
					$('.send-email-confirmation').hide('slow');
				}
				else {
					$.growl.error({title:"Email failure", message:"Could not send confirmation email."});

				}
       },
       error: function(rs, e) {
       		   console.log(rs.responseText);
       }
      });

}
// Returns text statistics for the specified editor by id
function getStats(id) {
    var body = tinymce.get(id).getBody(), text = tinymce.trim(body.innerText || body.textContent);

    return {
        chars: text.length,
        words: text.split(/[\w\u2019\'-]+/).length
    };
}
function ValidateCharacterLength() {
    // Check if the user has entered less than 1000 characters
    if (getStats('exp_input').chars > 4000) {
        $.growl.warning({title:"Too big", message: "Your post is too big, try to make it more compact."});
        return false;
    }
    return true;

}
function isotopize(){
    	var $container = $('.grid').isotope({
  			itemSelector: '.term-filtered',
  			percentPosition: true,
  			getSortData: {
      			posts: '.term-stats-number.explanations parseInt',
      			views: '.term-stats-number.term-views parseInt',
      			upvotes: '.likes-count.ups-hidden parseInt',
      			downvotes: '.likes-count.downs-hidden parseInt',
   			}
		});

		var iso = $container.data('isotope');
  		$container.isotope( 'reveal', iso.items );
}



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
