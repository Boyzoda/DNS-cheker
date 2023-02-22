import requests
from bs4 import BeautifulSoup
import dns.resolver

d = list(open('domain.txt', 'r'))
domains = []
for i in d:
    domains.append(i.strip())

with open("result.txt", "w") as f:
    for domain in domains:
        ns_records = []
        a_records = []
        if domain.endswith(".tj"):
            try:
                a = dns.resolver.query(domain, 'A')
                for adata in a:
                    a_records.append(str(adata))

                url = f"https://ismtj.co/whois/?domain={domain}"
                response = requests.get(url)
                soup = BeautifulSoup(response.content, "html.parser")
                hostname1 = soup.find('td', class_='subfield', text='Имя хоста:').find_next_sibling('td').next
                hostname2 = soup.find_all('td', class_='subfield', text='Имя хоста:')[1].find_next_sibling('td').next
                print(f"NS records for {domain} and A zapis: \n {hostname1} \n {hostname2}")
                f.write(f"NS records for {domain} and A zapis: \n {hostname1} \n {hostname2}\n")
                for a in a_records:
                    print(f"\n{a}")
                    f.write(f"{a}\n")
            except Exception as e:
                f.write(f"Error: {domain} - {e}\n")
        else:

            try:
                ns = dns.resolver.query(domain, 'NS')
                a = dns.resolver.query(domain, 'A')
                for nsdata in ns:
                    ns_records.append(str(nsdata))
                for adata in a:
                    a_records.append(str(adata))
            except Exception as e:
                print(f"Error: {domain} - {e}")
                f.write(f"Error: {domain} - {e}\n")

            print(f"NS records for {domain} and A zapis:")
            f.write(f"NS records for {domain} and A zapis:\n")
            for ns in ns_records:
                print(f"\t{ns}")
                f.write(f"\t{ns}\n")
            for a in a_records:
                print(f"\t{a}")
                f.write(f"\t{a}\n")
