require "editheader";
require "variables";
require "envelope";

if anyof (
    header :contains "To" "echo@dmz.worldskills.org"
) {
    if envelope :matches "from" "*" { set "sender_email" "${1}"; }
    if header :matches "subject" "*" { set "subject" "${1}"; }
    # Drop the original "From: and To:" header
    deleteheader "from";
    deleteheader "to";
    # Add a new "From: and To:" header
    addheader "From" "echo@dmz.worldskills.org";
    addheader "To" "${sender_email}";
    # Add subject
    addheader "Subject" "Echo: ${subject}";    
    redirect "${sender_email}";
}
#    redirect "jamie.oliver@dmz.worldskills.org";}
