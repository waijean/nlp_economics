import pytest

from scraper.web_scraper import get_article


@pytest.mark.parametrize(
    "test_url, expected_title, expected_article",
    [
        (
            "https://www.dailymail.co.uk/money/markets/article-3005742/TV-Gregg-s-firm-pays-38p-1-owed-creditors.html",
            "Gregg Wallace's firm pays 38p for every £1 owed to creditors after MasterChef host's restaurant folds",
            "Creditors owed cash following the collapse of the restaurant run by MasterChef host Gregg Wallace have received just 38p for every pound they were owed, according to liquidators. Wallace & Co, based in Putney, South-West London, closed last year owing its suppliers £150,000 after receiving poor reviews and failing to entice customers. The liquidators had hoped to give creditors 47p per £1 owed. But the company’s latest filings reveal that due to problems submitting final VAT and PAYE returns, and having to pay the tax office more than first estimated, there was only enough left to pay 38 per cent, or £57,000, leaving £93,000 unpaid. Wallace, 50, was himself owed £293,000 by the firm, with wholesalers and suppliers of catering equipment left out of pocket by thousands. This was the BBC presenter’s third firm to close within 12 months after the closure of Gregg’s Bar & Grill in Bermondsey, South-East London, which was branded a ‘travesty’ by critics, and West Veg greengrocers, trading as Secretts Direct.",
        ),
        (
            "https://www.dailymail.co.uk/money/markets/article-4344182/DAILY-BRIEFING-New-chairman-named-city-watchdog.html",
            "DAILY BRIEFING: New chairman named for city watchdog small business panel",
            "Small move The City watchdog has appointed a new chairman for its small business panel. Craig Errington, head of advice firm Wesleyan, will next month take the helm at the group which aims to give smaller finance firms a chance to share their views on rules set out by the Financial Conduct Authority. Rich pickings Arbuthnot Banking Group has unveiled a £227.6m profit for 2016, up from £29m a year earlier. This was largely down to the sale of Everyday Loans Group and a 33 per cent stake in Secure Trust Bank. Arbuthnot – which runs a private lender for the super-rich – hiked its total dividend to 356p per share, up from 29p in 2015. Double bubble Aim-listed double-glazing business Safestyle has toasted record sales and profits. The firm said sales in 2016 were up 9.5 per cent to £163.1m from £148.9m the year before while profits were up 9.7 per cent to £19.3m. Safestyle has also achieved its 12th consecutive year of market share growth and increased its dividend by 10.3 per cent. Steve Birmingham, chief executive, said: ‘The board remains confident of delivering growth over the year ahead.’ Safe arrival Low-cost airline Ryanair said 90 per cent of its flights arrived on time in February. The airline, which operated 46,000 flights last month, claimed that it had received less than two complaints per 1,000 customers. New names Vodafone has announced a series of top-level changes after the retirement of two board members. Nick Land, chairman of the audit and risk committee, and Philip Yea, senior independent director will not stand for re-election at the AGM in July after ten years. Replacing them will be David Nish and Val Gooding. US deal Healthcare tech firm Craneware has won a contract with a large hospital group in the US. Craneware, which specialises in software for healthcare billing and medicare compliance, said the deal was worth £2.9m. It will also bring £1.2m of extra revenue as an existing contract is extended. Talking shop A new lobby group for bankers, payments firms and credit card has announced it will be called UK Finance. It is being formed by a tie-up between six smaller organisations including the British Bankers’ Association, the Council of Mortgage Lenders and Financial Fraud Action UK. ",
        ),
        (
            "https://www.dailymail.co.uk/money/markets/article-6022435/FTSE-LIVE-RBS-pay-dividend-decade-British-Airways-owner-profits-off.html",
            "FTSE CLOSE: RBS to pay first dividend in a decade; BA owner's profits take off; pound at $1.30",
            "The FTSE 100 closed up 83.17 points at 7659.10 and the pound was at $1.30 against the dollar. Royal Bank of Scotland is set to pay its its first dividend in 10 years, despite bottom-line profits dropping in the first half of the year. Meanwhile, British Airways-owner IAG is toasting a 6.3 per cent rise in quarterly earnings as passenger numbers jumped and costs eased.  ",
        ),
        (
            "https://www.dailymail.co.uk/money/markets/article-4791510/MARKETS-CLOSE-Shares-tick-higher.html",
            "MARKETS CLOSE: Shares finish higher while Brexit Secretary David Davis unveils temporary EU customs plan",
            "London shares ticked higher as Brexit secretary David Davis set out his stall, calling for a new customs arrangement with the European Union. The UK has proposed setting up a customs union during an interim period after leaving the European Union, Davis has said. The interim customs agreement with the European Union after Brexit would allow the freest possible trade of goods. When asked on ITV television if Britain would have to pay to stay in the EU customs union temporarily, Brexit minister Davis said: 'No, I don't think (so). Well what happens in that interim period you have to leave to me to negotiate.'",
        ),
    ],
    ids=["normal_15", "daily_briefing_17", "ftse_live_18", "markets_close_17"],
)
def test_get_article(test_url, expected_title, expected_article):
    title, article = get_article(test_url)
    assert title == expected_title
    assert article == expected_article
