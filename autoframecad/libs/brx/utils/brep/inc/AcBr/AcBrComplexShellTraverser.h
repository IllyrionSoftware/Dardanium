// Property of Bricsys NV. All rights reserved.
// This file is part of the BRX SDK, and its use is subject to the terms
// of the BRX SDK license agreement.
/////////////////////////////////////////////////////////////////////////
#pragma once

#include "AcBr/AcBrTraverser.h"

class AcBrComplex;
class AcBrShell;
class AcBrBrepComplexTraverser;

class AcBrComplexShellTraverser: public AcBrTraverser
{
public:
    ACRX_DECLARE_MEMBERS(AcBrComplexShellTraverser);

    AcBrComplexShellTraverser();
    AcBrComplexShellTraverser(const AcBrComplexShellTraverser&);
    ~AcBrComplexShellTraverser();

    AcBr::ErrorStatus getComplex(AcBrComplex&) const;
    AcBr::ErrorStatus getShell(AcBrShell&) const;
    AcBr::ErrorStatus setComplex(const AcBrBrepComplexTraverser&);
    AcBr::ErrorStatus setComplex(const AcBrComplex&);
    AcBr::ErrorStatus setComplexAndShell(const AcBrShell&);
    AcBr::ErrorStatus setShell(const AcBrShell&);

    AcBrComplexShellTraverser& operator=(const AcBrComplexShellTraverser&);
};
