
$(document).ready(function(){
	
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



	$('.exp-body').each(function(){
		jQuery(this).linkify();
	});
	


	function challenge(challengee_id, term_id){
		$('#dialog-challenge-button-'+ challengee_id).addClass("button-bg-loader");
		var obj = {'challengee_id':challengee_id, 'term_id':term_id}
			$.ajax({
			           type: "POST",
			           url: "/simplenation/challenge/",
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
			                   alert(rs.responseText);
			            }
			});
	}

	function challengee_list(term_id){
		var obj = { 'term_id':term_id }
		$.ajax({
			           type: "POST",
			           url: "/simplenation/challengee_list/",
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
			                   alert(rs.responseText);
			            }
			});

	}

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
								if (data['notification_flag']){
									$('.notifications-indicator').html(data['num_of_unseen_notifications'])
								}
			            },
			            error: function(rs, e) {
			                   alert(rs.responseText);
			            }
			});

	}

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
			

	}, 50000);

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
			if(currentElement.text() == "explanations"){
				currentElement.addClass("top");
				sortUsingNestedTextDescending($('.terms-filtered-container'), ".term-filtered", "div.term-stats-number.explanations");
			}
			else{
				currentElement.addClass("views");
				sortUsingNestedTextDescending($('.terms-filtered-container'), ".term-filtered", "div.term-stats-number.term-views");
			}
			
		}

	});


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
			console.log(text);
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
			console.log(text);
			inputElement.val(text);
		}
	}


	function autocomplete_search(search_item){
			$('.global-search-form').append('<img class="global-search-loader" src="/static/images/loader.gif" width="15" height="15">');
			var obj = { 'search_item':search_item }
			$.ajax({
			           type: "POST",
			           url: "/simplenation/autocomplete_search/",
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
			                   alert(rs.responseText);
			            }
			});

	}


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

	

	function autocomplete_tag_search(search_item){
			$('.search-tags-wrapper').append('<img class="tag-search-loader" src="/static/images/loader.gif" width="15" height="15">');
			var obj = { 'search_item':search_item }
			$.ajax({
			           type: "POST",
			           url: "/simplenation/autocomplete_tag_search/",
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
			                   alert(rs.responseText);
			            }
			});

	}

	function tag_search(search_tag_item){
			$.ajax({
			           type: "GET",
			           url: "/simplenation/search_tags/",
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
			                   alert(rs.responseText);
			            }
			});

	}
	
			

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


	function chosen_tags_list(currently_pressed_tag){
			var tag_choose_list = {};
			var duplicate_prevent_count = 0;
			var count = 0;
			$('.tag-choose').each(function(){
					if ($(this).css('background-color') == 'rgb(0, 145, 194)') {
						if($(this).attr('data-tagname') != currently_pressed_tag){
							count = count + 1;
							var tagname = $(this).attr('data-tagname');
							tag_choose_list['tag_name_' + count] = tagname;
						}
						else {
							;
						}

					} 
					else {
						if($(this).attr('data-tagname') == currently_pressed_tag){

							if(duplicate_prevent_count == 0){
								count = count + 1;
								var tagname = $(this).attr('data-tagname');
								tag_choose_list['tag_name_' + count] = tagname;
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

	function tag_filter(count, tag_choose_list){
		$('.terms-filtered-container').html('<img src="/static/images/loader.gif" width="30" height="30">');
		if(count == 0)
				{

				var obj = { 'number_of_tags':count }
				$.ajax({
			           type: "POST",
			           url: "/simplenation/tag_select/",
			           contentType: 'application/json; charset=utf-8',
			           data: JSON.stringify(obj),
			           success: function(data) {
								$('.terms-filtered-container').html(data);
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
								$('.terms-filtered-container').html(data);
			            },
			            error: function(rs, e) {
			      
			                   alert(rs.responseText);
			            }
				});
				}

	}
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
			           url: "/simplenation/tag_deselect/",
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
				           url: "/simplenation/add_tags_to_term/",
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
		
	
	function update_favoree_list(term_id){
		var obj = { 'term_id' : term_id}
		$.ajax({
			           type: "POST",
			           url: "/simplenation/update_favoree_list/",
			           contentType: 'application/json; charset=utf-8',
			           data: JSON.stringify(obj),
			           success: function(data) {
			           			console.log(data);
							  	$('.favorite-dialog-block').html(data);
							  	var dialogAuthorTitle = $(".dialog-author-title");
     							dialogAuthorTitle.css("color","#0091c2");
	       						challengee_list(term_id);
			            },
			            error: function(rs, e) {
			                   alert(rs.responseText);
			            }
          });
	}


	function add_favourites_to_challenge(favoree_id, term_id)
	{
		var obj = { 'favoree_id': favoree_id}
		$.ajax({
			           type: "POST",
			           url: "/simplenation/add_favoree/",
			           contentType: 'application/json; charset=utf-8',
			           data: JSON.stringify(obj),
			           success: function(data) {
			           			if (data['success']){
			           				$.growl.notice({message:"Added to favourites."});
			           				update_favoree_list(term_id);  
			           			}
			           			else {
			           				$.growl.warning({message:data['no_success_message']});
			           			}
							     
			            },
			            error: function(rs, e) {
			                   alert(rs.responseText);
			            }
          });
	}

	function add_favourites(favoree_id)
	{
		var obj = { 'favoree_id': favoree_id}
		$.ajax({
			           type: "POST",
			           url: "/simplenation/add_favoree/",
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
			           			if (data['success']){
			           				$.growl({title:"Notice", message:"Removed from favourites."});     
			           			}
			           			else {
			           				$.growl.warning({message:data['no_success_message']});
			           			}
							  
			            },
			            error: function(rs, e) {
			                   alert(rs.responseText);
			            }
          });
	}

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


	function add_like(explanation_id)
	{

		var obj={'explanation_id':explanation_id}

		jQuery.ajax({
			           type: "POST",
			           url: "/simplenation/add_like/",
			           contentType: 'application/json; charset=utf-8',
			           data: JSON.stringify(obj),
			           success: function(data) {
							   $('#likes-count-'+explanation_id).html(data);  
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
							   $('#likes-count-'+explanation_id).html(data);  
			            },
			            error: function(rs, e) {
			                   alert(rs.responseText);
			            }
          });

	}

	
	$('.like-container').on('click', '.like_class', function(){

		var explanation_id = $(this).attr('data-expid');
		  if($(this).hasClass("liked")) {
		  	
			$('#likes-'+explanation_id).removeClass('liked');
			remove_like(explanation_id);
		  } else if ($(this).hasClass("not-registered")){
		  	$.growl.warning({ title: "Please Log In", message: "You need to sign in to like." });

		  } else {
		  	
			$('#likes-'+explanation_id).addClass('liked');
			add_like(explanation_id);
		  }

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

	function cancel_edition(explanation_id){
		var obj = {'explanation_id':explanation_id }

		jQuery.ajax({
           type: "POST",
           url: "/simplenation/cancel_edition/",
           contentType: 'application/json; charset=utf-8',
           data: JSON.stringify(obj),
           success: function(data) {
				   $('#pictures-container-'+explanation_id).html(data);
           },
           error: function(rs, e) {
                   alert(rs.responseText);
           }
          });

	}


	function add_picture(explanation_id){
		var data = new FormData($('#picture-form-'+explanation_id).get(0));

		$.ajax({
    		url: $('#picture-form-'+explanation_id).attr('action'),
    		type: $('#picture-form-'+explanation_id).attr('method'),
    		data: data,
    		cache: false,
    		processData: false,
    		contentType: false,
    		success: function(data) {
        		$('#pictures-container-'+explanation_id).html(data);
    		},
    		error: function(rs, e) {
			    alert(rs.responseText);
			}
		});

	}

	function remove_picture(explanation_id, picture_id){
		var obj = {'picture_id':picture_id }

		jQuery.ajax({
           type: "POST",
           url: "/simplenation/remove_picture/",
           contentType: 'application/json; charset=utf-8',
           data: JSON.stringify(obj),
           success: function(data) {
				   $('#pictures-container-'+explanation_id).html(data);
           },
           error: function(rs, e) {
                   alert(rs.responseText);
           }
          });

		

	}

	// Logic to handle removal of pictures
	$('.pictures-container').on('click', '.remove-picture',  function(){
		console.log('remove picture pressed');
			var explanation_id = $(this).attr('data-expid');
			var picture_id = $(this).attr('data-pictureid');
			
			remove_picture(explanation_id, picture_id);
	});


	


	// Logic to handle addition of pictures
	$('.picture-add').each(function(){
			var explanation_id = $(this).attr('data-expid');
			$('#pictures-container-'+explanation_id).on('change', '#picture-of-'+explanation_id,  function(){
					
					add_picture(explanation_id);
					
			});
	});

	$('.pictures-container').on('click', '.add-picture', function(){
		var explanation_id = $(this).attr('data-expid');
		$('#picture-of-'+explanation_id).click();
	});


	$('.pictures-container').on('click', '.picture-thumbnail', function(){
		console.log('picture-thumbnail pressed');
		var explanation_id = $(this).attr('data-expid');
		var picture_id = $(this).attr('data-pictureid');
		$('.gallery-element-'+explanation_id).Am2_SimpleSlider();
		$('#gallery-element-'+picture_id).click();

	});
	

	function readURL(input, preview_count) {
		
	    if (input.files && input.files[0]) {
	        var reader = new FileReader();
	        
	        reader.onload = function (e) {
	        	console.log($('#add-post-picture-preview-'+preview_count).attr('src'));
	            $('#add-post-picture-preview-'+preview_count).attr('src', e.target.result);
	        }

	        reader.readAsDataURL(input.files[0]);
	    }
	}
	
	


	$('.explanation-post-form').on( 'change', '.add-post-picture-input', function(){
			var preview_count = parseInt($(this).attr('data-count'), 10);
			readURL(this, preview_count);
			$('#preview-picture-'+preview_count).show();
			$('#add-post-picture-wrapper-'+preview_count).hide();
			preview_count = preview_count + 1;
			$('.add-post-pictures').append('<div class="add-post-picture preview" id="preview-picture-'+preview_count+'" style="display:none; overflow:hidden;"><img class="add-post-picture-placeholder preview" id="add-post-picture-preview-'+ preview_count +'" data-count="'+ preview_count +'" src="#"><button class="remove-post-picture" id="remove-post-picture-'+ preview_count +'" data-count="'+ preview_count +'" type="button" style="border: 0px;">x</button></div>');
			$('.add-post-pictures').append('<div class="add-post-picture" id="add-post-picture-wrapper-'+ preview_count +'"><input class="add-post-picture-input" id="add-post-picture-'+ preview_count +'" data-count="'+preview_count+'" type="file" name="pictures" style="display:none;"><img class="add-post-picture-placeholder" id="add-post-picture-placeholder-'+ preview_count +'" data-count="'+ preview_count +'" src="/static/images/add-photo@2x.png"></div>');
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


		var explanation_id = $(this).attr('data-expid');
		var body = $('#edit-input-'+ explanation_id).val();
		var signal = $(this).attr('data-signal');

		$.ajax({
			           type: "POST",
			           url: "/simplenation/edit_exp/",
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

	});

	$('.edit-option-buttons').on('click', '.delete-post-button', function(){

		var explanation_id = $(this).attr('data-expid');
		var signal = $(this).attr('data-signal');

				$.ajax({
			           type: "POST",
			           url: "/simplenation/edit_exp/",
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
		$('#edit-'+explanation_id).hide();
		$('#edit-text-'+explanation_id).show();
		$('#edit-option-'+explanation_id).show();
		$('#add-picture-of-'+explanation_id).show();

		$(".picture-container[data-expid='"+explanation_id+"']").each(function(){
				picture_id = $(this).attr('data-pictureid');
				$('#remove-picture-'+picture_id).show();
		});


	});



	function preview_profile_picture(input) {

	    if (input.files && input.files[0]) {
	        var reader = new FileReader();
	        reader.onload = function (e) {
	        	
	            $('.profile-registration-img').attr('src', e.target.result);
	        }

	        reader.readAsDataURL(input.files[0]);
	    }
	}

	$('.registration-form').on('change','.add-profile-picture', function(){

		$('.profile-registration-mask').show();
		preview_profile_picture(this);

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