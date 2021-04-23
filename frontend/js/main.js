$.ajaxSetup({
	beforeSend: function beforeSend(xhr, settings) {
		function getCookie(name) {
			let cookieValue = null;
			if (document.cookie && document.cookie !== '') {
				const cookies = document.cookie.split(';');
				for (let i = 0; i < cookies.length; i += 1) {
					const cookie = jQuery.trim(cookies[i]);
					if (cookie.substring(0, name.length + 1) === (`${name}=`)) {
						cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
						break;
					}
				}
			}
			return cookieValue;
		}

		if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
			xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
		}
	},
});

$("#create-new-post").on("click", function(e) {
	e.preventDefault();
	$(".new-post-modal").removeClass("hidden");
});

$("#cancel-new-post").on("click", function(e) {
	e.preventDefault();
	$(".new-post-modal").addClass("hidden");
});

$("#create-post").on("click", function(e) {
	e.preventDefault();
	const tag = $("#tag").val().trim();
	const text = $("#text").val().trim();
	const details = $("#details").val().trim();
	const $btn = $(this);

	if (!text.length) {
		return false;
	}

	$btn.prop("disabled", true).text("Posting!");

	$.ajax({
		type: "POST",
		url: $("#text").data("post-url"),
		data: {
			text: text,
			details: details,
			tag: tag,
		},
		success: (response) => {
			$(".new-post-modal").addClass("hidden");
			$("#post-container").prepend(response);
			$("#tag").val("");
			$("#text").val("");
			$("#details").val("");
			$btn.prop("disabled", false).text("Create Post");
		},
		error: (error) => {
			console.warn(error);
			$btn.prop("disabled", false).text("Error");
		}
	});
});

$(".follow-button").on("click", function(e) {
	e.preventDefault();
	$(this).prop("disabled", true);

	const action = $(this).attr("data-action");

	$.ajax({
		type: "POST",
		url: $(this).data("url"),
		data: {
			action: action,
			username: $(this).data("username"),
		},
		success: (response) => {
			$(".follow-text").text(response.wording);
			$(this).prop("disabled", false);
			$(this).attr("data-action", response.wording.toLowerCase());
		},
		error: (error) => {
			console.warn(error);
			$(this).prop("disabled", false);
		}
	});
});