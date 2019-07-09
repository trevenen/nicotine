# products: DNSMasq 
#           elsearch
#           git 
#           hdd 
#           katello
#           pims 
#           prxy 
#           puppet
#           SMTP 
#           ssr 
#           Talend
#           yum 

# DNSMasq
dnsmasq = None

# elsearch: must run in deathwish mode
# so epinephrine can't be administered
elsearch = None

# git
git = None

hdd = { 'hdd_di': 'di-HDD',
        'hdd_qa': 'qa-HDD',
        'hdd_ct': 'ct-HDD',
        'hdd_pr': 'pr-HDD
      }

# katello
katello = None

pims = { 'pims_di': 'di-pims',
         'pims_qa': 'qa-pims',
         'pims_ct': 'ct-pims',
         'pims_pr': 'pr-pims',
       }

# squids get patched on boot
# CFN user data or something
# similar
prxy = None

# puppet
puppet = None

# SMTP
smtp = None

# ssr
# these machines require
# manual patching and are
# not yet a nicotine patch
# candidate
ssr = None

# Talend (search)
talend = None

# Talend (SSR)
# requires manual patching
talend_ssr = None

# yum
yum = None
