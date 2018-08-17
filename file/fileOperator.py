str = 'applyDto = loanCreditPayApplyService.findApplingByRenterId(renterId);'

import re

flag = re.search(r'(.*)loanCreditPayApplyService.(.*)\(', str).group(0)
print(flag)