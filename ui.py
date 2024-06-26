from main import base, shares, reader, end
import streamlit as st
from PIL import Image
import os
import re

def write_html(pr_name, reg_name, link, st=None, rdr=False):
    global base
    global shares
    global reader
    html_file = open("snowflake_data_sharing.html", "w")

    # Update all provider names
    base = re.sub(r'ProviderName', pr_name, base)
    shares = re.sub(r'ProviderName', pr_name, shares)
    reader = re.sub(r'ProviderName', pr_name, reader)

    # Update all region names
    base = re.sub(r'ProviderRegion', reg_name, base)

    # Update link
    base = re.sub(r'SPN_ReferralLink', link, base)

    # Has steps, supports reader
    if st is not None and rdr is True:
        html = base + st + shares + reader + end
    elif st is not None:
        # Has steps, does not support reader
        html = base + st + shares + end
    elif rdr is True:
        html = base + shares + reader + end
    else:
        html = base + shares + end

    # close output file
    html_file.write(html)
    html_file.close()
    return html_file

def main():
    
    image = Image.open('./assets/image3.jpg')
    st.image('./assets/image3.jpg')
    
    st.title("Customize a Guidelines Doc for Sharing Data via Snowflake")

    st.write("Simplify the process of sharing data with your customers: give them a how-to-share document customized with your company's name and preferences. This app will create a set of data sharing guidelines to help your customer connect with you through their existing Snowflake account or by setting up a new Snowflake account.")

    st.markdown("[Click here to see a sample PDF.](https://www.snowflake.com/wp-content/uploads/2024/03/Sample-Doc-How-to-Use-Snowflake-to-Share-Data.pdf)")
    
    st.write("To get started, please fill out this form as completely as possible. The app will generate a customized HTML document that you can save as a PDF and send to your customers. You can return to this form and create additional versions as needed.")

    # Create a form
    with st.form(key='user_input_form'):

        # required
        st.markdown('**Provider Name (required)**')
        provider_name = st.text_input('How do you want to refer to your organization in this document? The text you enter will be used to customize the document.')
        
        # required
        st.markdown('**Provider Region (required)**')
        provider_region = st.text_input('A customer will use this value to select a cloud region for their own Snowflake instance. Please check the list of supported Snowflake regions at https://docs.snowflake.com/en/user-guide/intro-regions and populate this field with your relevant region name (for example: "AWS US East (Ohio)"). This will make it easy for the customer to match it to the region options they see during account setup.')

        # optional
        st.markdown('**SPN Referral Link (if available)**')
        spn_referral_link = st.text_input('If you have a personalized link to the Snowflake free trial for Snowflake referral partners, insert it here. To learn more about this program, contact your Snowflake account team. If you leave this field blank, your customer will be directed to the default Snowflake trial signup page.')

        # optional
        st.markdown('**Instructions to submit Snowflake ID**')
        desc_steps = '''Customers will need to send you their Snowflake account identifier before you can share data with them. Please provide written instructions for how they should give you their account identifier. For example: "Send your account identifier to [email address]” or “Contact your account rep and give them your account ID."'''

        steps = st.text_area(desc_steps)

        # optional
        reader = st.checkbox("Check this box if you will support reader accounts for companies that don't have a Snowflake account.")
        
        submit_button = st.form_submit_button('Submit')
       
    # Capture inputs
    # When button is clicked:
    # Check for errors
    # Check for optional fields set
    # Generate the file with required fields and optional fields
    if submit_button:
        # Validate inputs when button is clicked
        if provider_name == '' or provider_region == '':
            return st.error("File not generated. Required field is not set.")
        
        if spn_referral_link == '':
            spn_referral_link = '<a href="https://signup.snowflake.com/">signup.snowflake.com</a>'
        else:
            spn_referral_link = f'<a href="{spn_referral_link}">{spn_referral_link}</a>'

        # This won't render them in list order, instead 
        # in block rendering, and it's hard to read
        if steps != '':
            steps = "<p>" + steps + "</p>"

        if steps != '' and reader:
            # render everything
            write_html(provider_name, provider_region, spn_referral_link, steps, reader)
        elif steps != '':
            # render portion
            write_html(provider_name, provider_region, spn_referral_link, steps)
        elif reader:
            # render portion
            write_html(provider_name, provider_region, spn_referral_link, reader)
        else:
            # render base
            write_html(provider_name, provider_region, spn_referral_link)

        f = open("snowflake_data_sharing.html", "r")

        st.download_button(label="Download HTML file", data=f, file_name="snowflake_data_sharing.html")
        st.write("Once the download is complete, open the HTML file and save the page as a PDF with the file name of your choice. You can then send the PDF to your customer.")

if __name__ == "__main__":
    main()
