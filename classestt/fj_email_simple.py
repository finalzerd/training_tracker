__author__ = "noahpro"

from typing import List

from .email import Email

class FJEmailSimple(Email):
  def __init__(self, to: List[str] = None, cc: List[str] = None, bcc: List[str] = None,
                 subject: str = "",
                 title: str = "",
                 text: str = "") -> None:

        self.title = title
        self.text = text
        
        self.instagram_image_link: str = "https://www.edigitalagency.com.au/wp-content/uploads/new-Instagram-logo-white-glyph-1200x1199.png"

        html: str = self.build_html()
        super().__init__(to=to, cc=cc, bcc=bcc, subject=subject, html=html)

  def build_html(self) -> str:
    return self.get_header_html() + self.get_footer_html()

  def get_header_html(self) -> str:
      return f"""<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">

<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="x-apple-disable-message-reformatting">
<title></title>
<!--[if mso]>
<style>
  table {{border-collapse:collapse;border-spacing:0;border:none;margin:0;}}
  div, td {{padding:0;}}
  div {{margin:0 !important;}}
</style>
<noscript>
  <xml>
    <o:OfficeDocumentSettings>
      <o:PixelsPerInch>96</o:PixelsPerInch>
    </o:OfficeDocumentSettings>
  </xml>
</noscript>
<![endif]-->
<style>
  table,
  td,
  div,
  h1,
  p {{
    font-family: Arial, sans-serif;
  }}

  @media screen and (max-width: 530px) {{
    .unsub {{
      display: block;
      padding: 8px;
      margin-top: 14px;
      border-radius: 6px;
      background-color: #555555;
      text-decoration: none !important;
      font-weight: bold;
    }}

    .col-lge {{
      max-width: 100% !important;
    }}
  }}

  @media screen and (min-width: 531px) {{
    .col-sml {{
      max-width: 30% !important;
    }}

    .col-lge {{
      max-width: 70% !important;
    }}
  }}
</style>
</head>

<body style="margin:0;padding:0;word-spacing:normal;background-color:#263844;">
<div role="article" aria-roledescription="email" lang="en"
  style="text-size-adjust:100%;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;background-color:#263844;">
  <table role="presentation" style="width:100%;border:none;border-spacing:0;">
    <tr>
      <td align="center" style="padding:0;">
        <!--[if mso]>
        <table role="presentation" align="center" style="width:600px;">
        <tr>
        <td>
        <![endif]-->
        <table role="presentation"
          style="width:94%;max-width:600px;border:none;border-spacing:0;text-align:left;font-family:Arial,sans-serif;font-size:16px;line-height:22px;color:#363636;">
          <!--FJ Logo-->
          <tr>
            <td style="padding:40px 30px 30px 30px;text-align:center;font-size:24px;font-weight:bold;">
              <a href="https://fischerjordan.com/" style="text-decoration:none;"><img
                  src="https://fischerjordan.com/wp-content/uploads/2018/12/FJ-Logo-horizontal-white-1.png"
                  width="200" alt="Logo"
                  style="width:200px;max-width:80%;height:auto;border:none;text-decoration:none;color:#ffffff;"></a>
            </td>
          </tr>
          <!--Summary Text-->
          <tr>
            <td style="padding:30px;background-color:#ffffff;">
              <h1
                style="margin-top:0;margin-bottom:16px;text-align:center;font-size:26px;line-height:32px;font-weight:bold;letter-spacing:-0.02em;">
                {self.title}</h1>
              <p style="margin:0;"><br>{self.text}</p>
            </td>

          </tr>"""

  def get_footer_html(self) -> str:
      return f"""
                  <!--Social links-->
                      <tr>
                      <td style="padding:30px;text-align:center;font-size:12px;">
                          <p style="margin:0 0 8px 0;">
                              <a href="https://www.instagram.com/fischerjordan_ny/?hl=en" style="text-decoration:none;">
                                  <img src="{self.instagram_image_link}" width="40" height="40" alt="f"
                                  style="display:inline-block;color:#cccccc;"></a>
                              <a href="https://www.linkedin.com/company/fischerjordan/mycompany/"
                                  style="text-decoration:none;"><img src="https://iconsplace.com/wp-content/uploads/_icons/ffffff/256/png/linkedin-icon-18-256.png" width="40"
                                  height="40" alt="t" style="display:inline-block;margin:0px 4px;color:#1f276d;"></a>
                              <a href="https://mobile.twitter.com/fischerjordanny"
                                  style="text-decoration:none;"><img src="https://assets.codepen.io/210284/twitter_1.png" width="40"
                                  height="40" alt="t" style="display:inline-block;color:#1f276d;"></a>

                          </p>
                          <p style="margin:0;font-size:14px;line-height:20px;color: #C5972C;">&reg; FischerJordan, LLC | 125
                          Maiden Lane, Suite 312, New York, NY 10038
                          </p>
                      </td>
                      </tr>
                  </table>
                  <!--[if mso]>
                  </td>
                  </tr>
                  </table>
                  <![endif]-->
                  </td>
              </tr>
              </table>
          </div>
          </body>

          </html>"""
