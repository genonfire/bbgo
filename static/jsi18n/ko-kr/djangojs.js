

(function(globals) {

  var django = globals.django || (globals.django = {});

  
  django.pluralidx = function(n) {
    var v=0;
    if (typeof(v) == 'boolean') {
      return v ? 1 : 0;
    } else {
      return v;
    }
  };
  

  /* gettext library */

  django.catalog = django.catalog || {};
  
  var newcatalog = {
    "%(sel)s of %(cnt)s selected": [
      "%(sel)s\uac1c\uac00 %(cnt)s\uac1c \uc911\uc5d0 \uc120\ud0dd\ub428."
    ], 
    "6 a.m.": "\uc624\uc804 6\uc2dc", 
    "6 p.m.": "\uc624\ud6c4 6\uc2dc", 
    "Alarm for your activity.": "\uc54c\ub9bc\uc744 \ud655\uc778\ud574 \uc8fc\uc138\uc694.", 
    "Alphabet Number _ - . are only available.": "\uc601\ubb38 \uc22b\uc790 \ud2b9\uc218\ubb38\uc790(_ - .)\ub9cc \uac00\ub2a5\ud569\ub2c8\ub2e4.", 
    "Alphabet and number only.": "\uc601\ubb38 \uc22b\uc790\ub9cc \uac00\ub2a5\ud569\ub2c8\ub2e4.", 
    "Already exist.": "\uc774\ubbf8 \uc874\uc7ac\ud569\ub2c8\ub2e4.", 
    "Already expired.": "\uc774\ubbf8 \ub9cc\ub8cc\ub418\uc5c8\uc2b5\ub2c8\ub2e4.", 
    "Already joined.": "\uc774\ubbf8 \ucc38\uc5ec\uc911\uc785\ub2c8\ub2e4.", 
    "Already scrapped.": "\uc774\ubbf8 \uc2a4\ud06c\ub7a9\ud55c \uae00\uc785\ub2c8\ub2e4.", 
    "April": "4\uc6d4", 
    "Are you sure to cancel recruitment?": "\ubaa8\uc9d1\uc744 \ucde8\uc18c\ud558\uc2dc\uaca0\uc2b5\ub2c8\uae4c?", 
    "Are you sure to delete all?": "\ubaa8\ub450 \uc0ad\uc81c\ud558\uc2dc\uaca0\uc2b5\ub2c8\uae4c?", 
    "Are you sure to delete old messages?": "\uc624\ub798\ub41c \ucabd\uc9c0\ub97c \ubaa8\ub450 \uc0ad\uc81c\ud558\uc2dc\uaca0\uc2b5\ub2c8\uae4c?", 
    "Are you sure to delete this article?": "\uc815\ub9d0\ub85c \uc0ad\uc81c\ud558\uc2dc\uaca0\uc2b5\ub2c8\uae4c?", 
    "Are you sure to delete this comment?": "\uc815\ub9d0\ub85c \uc0ad\uc81c\ud558\uc2dc\uaca0\uc2b5\ub2c8\uae4c?", 
    "Are you sure to delete this conversation?": "\ub300\ud654\ub97c \uc0ad\uc81c\ud558\uc2dc\uaca0\uc2b5\ub2c8\uae4c?", 
    "Are you sure to delete this message?": "\ucabd\uc9c0\ub97c \uc0ad\uc81c\ud558\uc2dc\uaca0\uc2b5\ub2c8\uae4c?", 
    "Are you sure to delete your profile?": "\uc815\ub9d0\ub85c \ud0c8\ud1f4\ud558\uc2dc\uaca0\uc2b5\ub2c8\uae4c?", 
    "Are you sure to delete?": "\uc815\ub9d0\ub85c \uc0ad\uc81c\ud558\uc2dc\uaca0\uc2b5\ub2c8\uae4c?", 
    "Are you sure to finish recruitment?": "\ubaa8\uc9d1\uc744 \ub9c8\uac10\ud558\uc2dc\uaca0\uc2b5\ub2c8\uae4c?", 
    "Are you sure to kick this player?": "\uc815\ub9d0\ub85c \uac15\ud1f4\ud558\uc2dc\uaca0\uc2b5\ub2c8\uae4c?", 
    "Are you sure to leave this party?": "\ud30c\ud2f0\ub97c \ub5a0\ub098\uc2dc\uaca0\uc2b5\ub2c8\uae4c?", 
    "Are you sure to quit editing?": "\uae00\uc791\uc131\uc744 \uadf8\ub9cc\ub450\uace0 \ub098\uac00\uc2dc\uaca0\uc2b5\ub2c8\uae4c?", 
    "Are you sure to register this IP address to spam?": "\uc774 IP \uc8fc\uc18c\ub97c \uc2a4\ud338\uc5d0 \ub4f1\ub85d\ud558\uc2dc\uaca0\uc2b5\ub2c8\uae4c?", 
    "Are you sure to restore this article?": "\uc815\ub9d0\ub85c \ubcf5\uad6c \ud558\uc2dc\uaca0\uc2b5\ub2c8\uae4c?", 
    "Are you sure to resume recruitment?": "\ubaa8\uc9d1\uc744 \uc7ac\uac1c\ud558\uc2dc\uaca0\uc2b5\ub2c8\uae4c?", 
    "August": "8\uc6d4", 
    "Available %s": "\uc774\uc6a9 \uac00\ub2a5\ud55c %s", 
    "Bookmark saved.": "\ubd81\ub9c8\ud06c \uc800\uc7a5\ub428", 
    "Cancel": "\ucde8\uc18c", 
    "Choose": "\uc120\ud0dd", 
    "Choose a Date": "\uc2dc\uac04 \uc120\ud0dd", 
    "Choose a Time": "\uc2dc\uac04 \uc120\ud0dd", 
    "Choose a time": "\uc2dc\uac04 \uc120\ud0dd", 
    "Choose all": "\ubaa8\ub450 \uc120\ud0dd", 
    "Chosen %s": "\uc120\ud0dd\ub41c %s", 
    "Click to choose all %s at once.": "\ud55c\ubc88\uc5d0 \ubaa8\ub4e0 %s \ub97c \uc120\ud0dd\ud558\ub824\uba74 \ud074\ub9ad\ud558\uc138\uc694.", 
    "Click to remove all chosen %s at once.": "\ud55c\ubc88\uc5d0 \uc120\ud0dd\ub41c \ubaa8\ub4e0 %s \ub97c \uc81c\uac70\ud558\ub824\uba74 \ud074\ub9ad\ud558\uc138\uc694.", 
    "Copied to clipboard.": "\ud074\ub9bd\ubcf4\ub4dc\uc5d0 \ubcf5\uc0ac\ud588\uc2b5\ub2c8\ub2e4.", 
    "December": "12\uc6d4", 
    "Enter alias, more than 2 characters.": "\ubcc4\uce6d\uc744 2\uae00\uc790 \uc774\uc0c1 \uc785\ub825\ud558\uc138\uc694.", 
    "Enter comment here.": "\ub313\uae00\uc744 \uc785\ub825\ud574 \uc8fc\uc138\uc694.", 
    "Enter name here.": "\uc774\ub984\uc744 \uc785\ub825\ud574 \uc8fc\uc138\uc694.", 
    "Enter original URL.": "\uc6d0\ubcf8 URL\uc744 \uc785\ub825\ud558\uc138\uc694.", 
    "Error!": "\uc798\ubabb!", 
    "Error! Please check bookmarks limitation.": "\uc5d0\ub7ec! \ubd81\ub9c8\ud06c \uac1c\uc218 \uc81c\ud55c\uc744 \ub118\uacbc\ub294\uc9c0 \ud655\uc778\ud574 \uc8fc\uc138\uc694.", 
    "Exist alias. Please use different alias.": "\uc874\uc7ac\ud558\ub294 \ubcc4\uce6d\uc785\ub2c8\ub2e4. \ub2e4\ub978 \uc774\ub984\uc744 \uc0ac\uc6a9\ud574 \ubcf4\uc138\uc694.", 
    "Extended.": "\uc5f0\uc7a5\ub418\uc5c8\uc2b5\ub2c8\ub2e4.", 
    "Failed to send E-mail. Please try again later.": "\uc774\uba54\uc77c \ubc1c\uc1a1 \uc2e4\ud328. \ub098\uc911\uc5d0 \ub2e4\uc2dc \uc2dc\ub3c4\ud574 \uc8fc\uc138\uc694.", 
    "February": "2\uc6d4", 
    "Filter": "\ud544\ud130", 
    "Hide": "\uac10\ucd94\uae30", 
    "ID for this platform must exist in your user information.": "\ud68c\uc6d0\uc815\ubcf4\uc5d0 \ud574\ub2f9 \uae30\uc885\uc758 \uc544\uc774\ub514\uac00 \uc9c0\uc815\ub418\uc5b4 \uc788\uc5b4\uc57c \uc2ac\ub86f\uc5d0 \ucc38\uc5ec\ud560 \uc218 \uc788\uc2b5\ub2c8\ub2e4.", 
    "January": "1\uc6d4", 
    "July": "7\uc6d4", 
    "June": "6\uc6d4", 
    "March": "3\uc6d4", 
    "Master keys are different each other.": "\ub9c8\uc2a4\ud130\ud0a4\uac00 \uc11c\ub85c \ub2e4\ub985\ub2c8\ub2e4.", 
    "May": "5\uc6d4", 
    "Midnight": "\uc790\uc815", 
    "Mind the chracter length limitation.": "\uae00\uc790\uc218 \uc81c\ud55c\uc744 \uc9c0\ucf1c\uc8fc\uc138\uc694.", 
    "New masker key is same as current key.": "\uae30\uc874\uc758 \ub9c8\uc2a4\ud130\ud0a4\uc640 \ub3d9\uc77c\ud55c \ud0a4\ub97c \uc785\ub825\ud588\uc2b5\ub2c8\ub2e4.", 
    "Noon": "\uc815\uc624", 
    "Not changed.": "\ubcc0\uacbd\uc0ac\ud56d\uc774 \uc5c6\uc2b5\ub2c8\ub2e4.", 
    "Note: You are %s hour ahead of server time.": [
      "Note: \uc11c\ubc84 \uc2dc\uac04\ubcf4\ub2e4 %s \uc2dc\uac04 \ube60\ub985\ub2c8\ub2e4."
    ], 
    "Note: You are %s hour behind server time.": [
      "Note: \uc11c\ubc84 \uc2dc\uac04\ubcf4\ub2e4 %s \uc2dc\uac04 \ub2a6\uc740 \uc2dc\uac04\uc785\ub2c8\ub2e4."
    ], 
    "November": "11\uc6d4", 
    "Now": "\ud604\uc7ac", 
    "Number only!": "\uc22b\uc790\ub9cc \uac00\ub2a5\ud569\ub2c8\ub2e4!", 
    "October": "10\uc6d4", 
    "Party full.": "\ud30c\ud2f0 \ubaa8\uc9d1\uc774 \ub9c8\uac10\ub418\uc5c8\uc2b5\ub2c8\ub2e4.", 
    "Passwords are different each other.": "\ube44\ubc00\ubc88\ud638\uac00 \uc11c\ub85c \ub2e4\ub985\ub2c8\ub2e4.", 
    "Please consent to Terms.": "\uc57d\uad00\uc5d0 \ub3d9\uc758\ud574 \uc8fc\uc138\uc694.", 
    "Please don't leave your team behind.": "\ud30c\ud2f0\uc6d0\ub4e4\uc744 \ub450\uace0 \ub5a0\ub098\uc9c0 \ub9c8\uc138\uc694.", 
    "Please fill all bold text which mean mandatory.": "\uad75\uc740 \uae00\uc528\ub294 \ud544\uc218\ud56d\ubaa9\uc73c\ub85c \uaf2d \uc785\ub825\ud574\uc57c \ud569\ub2c8\ub2e4.", 
    "Please fill the contents.": "\ub0b4\uc6a9\uc744 \uc785\ub825\ud574 \uc8fc\uc138\uc694.", 
    "Please fill the subject.": "\uc81c\ubaa9\uc744 \uc785\ub825\ud574 \uc8fc\uc138\uc694.", 
    "Please input 2 or more characters.": "\ub450 \uae00\uc790 \uc774\uc0c1 \uc785\ub825\ud574 \uc8fc\uc138\uc694.", 
    "Please input correct E-mail address.": "\uc62c\ubc14\ub978 \uc774\uba54\uc77c \uc8fc\uc18c\ub97c \uc785\ub825\ud574 \uc8fc\uc138\uc694.", 
    "Please input correct IP address.": "\uc62c\ubc14\ub978 IP \uc8fc\uc18c\ub97c \uc785\ub825\ud574 \uc8fc\uc138\uc694.", 
    "Please input verification code correctly.": "\uc62c\ubc14\ub978 \uc778\uc99d\ucf54\ub4dc\ub97c \ub123\uc5b4\uc8fc\uc138\uc694.", 
    "Please select correct image.": "\uc62c\ubc14\ub978 \uc774\ubbf8\uc9c0 \ud30c\uc77c\uc744 \uc120\ud0dd\ud574 \uc8fc\uc138\uc694.", 
    "Please show some respect.": "\uc11c\ub85c\uc5d0 \ub300\ud55c \ubc30\ub824\uc640 \uc874\uc911\uc744 \ubcf4\uc5ec\uc8fc\uc138\uc694.", 
    "Recruitment canceled.": "\ud30c\ud2f0\ud300 \ubaa8\uc9d1\uc774 \ucde8\uc18c\ub418\uc5c8\uc2b5\ub2c8\ub2e4.", 
    "Remove": "\uc0ad\uc81c", 
    "Remove all": "\ubaa8\ub450 \uc81c\uac70", 
    "Reply to warning article is not available.": "\uc2e0\uace0\uc811\uc218\ub41c \uac8c\uc2dc\ubb3c\uc5d0\ub294 \ub313\uae00\uc744 \ub2ec \uc218 \uc5c6\uc2b5\ub2c8\ub2e4.", 
    "Require login": "\ud68c\uc6d0\ub9cc \uac00\ub2a5\ud569\ub2c8\ub2e4.", 
    "Saved successfully.": "\uc800\uc7a5 \uc131\uacf5.", 
    "Selected image is too big. size limit: ": "\uc774\ubbf8\uc9c0\uac00 \ub108\ubb34 \ud07d\ub2c8\ub2e4. \uc0ac\uc774\uc988 \uc81c\ud55c: ", 
    "Send message": "\ucabd\uc9c0 \ubcf4\ub0b4\uae30", 
    "September": "9\uc6d4", 
    "Show": "\ubcf4\uae30", 
    "Show new player": "\uc0c8\ub85c \ucc38\uc5ec\ud55c \ud50c\ub808\uc774\uc5b4", 
    "Show new replies": "\uc2e0\uaddc \ub313\uae00 \ubcf4\uae30", 
    "Show user article": "\uc791\uc131\uae00 \ubcf4\uae30", 
    "Show user reply": "\uc791\uc131\ub313\uae00 \ubcf4\uae30", 
    "That player is not a member of this party.": "\ud30c\ud2f0\uc758 \uc77c\uc6d0\uc774 \uc544\ub2d9\ub2c8\ub2e4.", 
    "This is the list of available %s. You may choose some by selecting them in the box below and then clicking the \"Choose\" arrow between the two boxes.": "\uc0ac\uc6a9 \uac00\ub2a5\ud55c %s \uc758 \ub9ac\uc2a4\ud2b8 \uc785\ub2c8\ub2e4.  \uc544\ub798\uc758 \uc0c1\uc790\uc5d0\uc11c \uc120\ud0dd\ud558\uace0 \ub450 \uc0c1\uc790 \uc0ac\uc774\uc758 \"\uc120\ud0dd\" \ud654\uc0b4\ud45c\ub97c \ud074\ub9ad\ud558\uc5ec \uba87 \uac00\uc9c0\ub97c \uc120\ud0dd\ud560 \uc218 \uc788\uc2b5\ub2c8\ub2e4.", 
    "This is the list of chosen %s. You may remove some by selecting them in the box below and then clicking the \"Remove\" arrow between the two boxes.": "\uc120\ud0dd\ub41c %s \ub9ac\uc2a4\ud2b8 \uc785\ub2c8\ub2e4.  \uc544\ub798\uc758 \uc0c1\uc790\uc5d0\uc11c \uc120\ud0dd\ud558\uace0 \ub450 \uc0c1\uc790 \uc0ac\uc774\uc758 \"\uc81c\uac70\" \ud654\uc0b4\ud45c\ub97c \ud074\ub9ad\ud558\uc5ec \uc77c\ubd80\ub97c \uc81c\uac70 \ud560 \uc218 \uc788\uc2b5\ub2c8\ub2e4.", 
    "Today": "\uc624\ub298", 
    "Tomorrow": "\ub0b4\uc77c", 
    "Type into this box to filter down the list of available %s.": "\uc0ac\uc6a9 \uac00\ub2a5\ud55c %s \ub9ac\uc2a4\ud2b8\ub97c \ud544\ud130\ub9c1\ud558\ub824\uba74 \uc774 \uc0c1\uc790\uc5d0 \uc785\ub825\ud558\uc138\uc694.", 
    "Unable to join to deleted recruitment.": "\uc0ad\uc81c\ub41c \ubaa8\uc9d1\uc5d0\ub294 \ucc38\uc5ec\ud560 \uc218 \uc5c6\uc2b5\ub2c8\ub2e4.", 
    "Verification failure. Please check verification code again.": "\uc778\uc99d\uc2e4\ud328. \uc778\uc99d\ucf54\ub4dc\ub97c \ub2e4\uc2dc \ud655\uc778\ud574 \uc8fc\uc138\uc694.", 
    "Verified successfully.": "\uc778\uc99d \uc131\uacf5.", 
    "Yesterday": "\uc5b4\uc81c", 
    "You are not a member of this party.": "\uc774 \ud30c\ud2f0\uc758 \uc77c\uc6d0\uc774 \uc544\ub2d9\ub2c8\ub2e4.", 
    "You are not the party leader.": "\ud30c\ud2f0\uc758 \ub9ac\ub354\uac00 \uc544\ub2d9\ub2c8\ub2e4.", 
    "You have selected an action, and you haven't made any changes on individual fields. You're probably looking for the Go button rather than the Save button.": "\uac1c\ubcc4 \ud544\ub4dc\uc5d0 \uc544\ubb34\ub7f0 \ubcc0\uacbd\uc774 \uc5c6\ub294 \uc0c1\ud0dc\ub85c \uc561\uc158\uc744 \uc120\ud0dd\ud588\uc2b5\ub2c8\ub2e4. \uc800\uc7a5 \ubc84\ud2bc\uc774 \uc544\ub2c8\ub77c \uc9c4\ud589 \ubc84\ud2bc\uc744 \ucc3e\uc544\ubcf4\uc138\uc694.", 
    "You have selected an action, but you haven't saved your changes to individual fields yet. Please click OK to save. You'll need to re-run the action.": "\uac1c\ubcc4 \ud544\ub4dc\uc758 \uac12\ub4e4\uc744 \uc800\uc7a5\ud558\uc9c0 \uc54a\uace0 \uc561\uc158\uc744 \uc120\ud0dd\ud588\uc2b5\ub2c8\ub2e4. OK\ub97c \ub204\ub974\uba74 \uc800\uc7a5\ub418\uba70, \uc561\uc158\uc744 \ud55c \ubc88 \ub354 \uc2e4\ud589\ud574\uc57c \ud569\ub2c8\ub2e4.", 
    "You have unsaved changes on individual editable fields. If you run an action, your unsaved changes will be lost.": "\uac1c\ubcc4 \ud3b8\uc9d1 \uac00\ub2a5\ud55c \ud544\ub4dc\uc5d0 \uc800\uc7a5\ub418\uc9c0 \uc54a\uc740 \uac12\uc774 \uc788\uc2b5\ub2c8\ub2e4. \uc561\uc158\uc744 \uc218\ud589\ud558\uba74 \uc800\uc7a5\ub418\uc9c0 \uc54a\uc740 \uac12\ub4e4\uc744 \uc783\uc5b4\ubc84\ub9ac\uac8c \ub429\ub2c8\ub2e4.", 
    "You've scrapped this article.": "\uc2a4\ud06c\ub7a9 \ud588\uc2b5\ub2c8\ub2e4.", 
    "one letter Friday\u0004F": "\uae08", 
    "one letter Monday\u0004M": "\uc6d4", 
    "one letter Saturday\u0004S": "\ud1a0", 
    "one letter Sunday\u0004S": "\uc77c", 
    "one letter Thursday\u0004T": "\ubaa9", 
    "one letter Tuesday\u0004T": "\ud654", 
    "one letter Wednesday\u0004W": "\uc218", 
    "scrap": "\uc2a4\ud06c\ub7a9", 
    "submit": "\ub4f1\ub85d", 
    "user info": "\ud68c\uc6d0 \uc815\ubcf4"
  };
  for (var key in newcatalog) {
    django.catalog[key] = newcatalog[key];
  }
  

  if (!django.jsi18n_initialized) {
    django.gettext = function(msgid) {
      var value = django.catalog[msgid];
      if (typeof(value) == 'undefined') {
        return msgid;
      } else {
        return (typeof(value) == 'string') ? value : value[0];
      }
    };

    django.ngettext = function(singular, plural, count) {
      var value = django.catalog[singular];
      if (typeof(value) == 'undefined') {
        return (count == 1) ? singular : plural;
      } else {
        return value[django.pluralidx(count)];
      }
    };

    django.gettext_noop = function(msgid) { return msgid; };

    django.pgettext = function(context, msgid) {
      var value = django.gettext(context + '\x04' + msgid);
      if (value.indexOf('\x04') != -1) {
        value = msgid;
      }
      return value;
    };

    django.npgettext = function(context, singular, plural, count) {
      var value = django.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
      if (value.indexOf('\x04') != -1) {
        value = django.ngettext(singular, plural, count);
      }
      return value;
    };

    django.interpolate = function(fmt, obj, named) {
      if (named) {
        return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
      } else {
        return fmt.replace(/%s/g, function(match){return String(obj.shift())});
      }
    };


    /* formatting library */

    django.formats = {
    "DATETIME_FORMAT": "Y\ub144 n\uc6d4 j\uc77c g:i A", 
    "DATETIME_INPUT_FORMATS": [
      "%Y-%m-%d %H:%M:%S", 
      "%Y-%m-%d %H:%M:%S.%f", 
      "%Y-%m-%d %H:%M", 
      "%Y-%m-%d", 
      "%m/%d/%Y %H:%M:%S", 
      "%m/%d/%Y %H:%M:%S.%f", 
      "%m/%d/%Y %H:%M", 
      "%m/%d/%Y", 
      "%m/%d/%y %H:%M:%S", 
      "%m/%d/%y %H:%M:%S.%f", 
      "%m/%d/%y %H:%M", 
      "%m/%d/%y", 
      "%Y\ub144 %m\uc6d4 %d\uc77c %H\uc2dc %M\ubd84 %S\ucd08", 
      "%Y\ub144 %m\uc6d4 %d\uc77c %H\uc2dc %M\ubd84"
    ], 
    "DATE_FORMAT": "Y\ub144 n\uc6d4 j\uc77c", 
    "DATE_INPUT_FORMATS": [
      "%Y-%m-%d", 
      "%m/%d/%Y", 
      "%m/%d/%y", 
      "%Y\ub144 %m\uc6d4 %d\uc77c"
    ], 
    "DECIMAL_SEPARATOR": ".", 
    "FIRST_DAY_OF_WEEK": "0", 
    "MONTH_DAY_FORMAT": "n\uc6d4 j\uc77c", 
    "NUMBER_GROUPING": "3", 
    "SHORT_DATETIME_FORMAT": "Y-n-j H:i", 
    "SHORT_DATE_FORMAT": "Y-n-j.", 
    "THOUSAND_SEPARATOR": ",", 
    "TIME_FORMAT": "A g:i", 
    "TIME_INPUT_FORMATS": [
      "%H:%M:%S", 
      "%H:%M:%S.%f", 
      "%H:%M", 
      "%H\uc2dc %M\ubd84 %S\ucd08", 
      "%H\uc2dc %M\ubd84"
    ], 
    "YEAR_MONTH_FORMAT": "Y\ub144 n\uc6d4"
  };

    django.get_format = function(format_type) {
      var value = django.formats[format_type];
      if (typeof(value) == 'undefined') {
        return format_type;
      } else {
        return value;
      }
    };

    /* add to global namespace */
    globals.pluralidx = django.pluralidx;
    globals.gettext = django.gettext;
    globals.ngettext = django.ngettext;
    globals.gettext_noop = django.gettext_noop;
    globals.pgettext = django.pgettext;
    globals.npgettext = django.npgettext;
    globals.interpolate = django.interpolate;
    globals.get_format = django.get_format;

    django.jsi18n_initialized = true;
  }

}(this));

