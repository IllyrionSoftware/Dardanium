#ifndef AC_BRHIT_H
#define AC_BRHIT_H 1
//
//  Copyright 2024 Autodesk, Inc.  All rights reserved.
//
//  Use of this software is subject to the terms of the Autodesk license 
//  agreement provided at the time of installation or download, or which 
//  otherwise accompanies this software in either electronic or hard copy form.   
//
// DESCRIPTION:
//
// The AcBrHit class is the interface class for hits generated by
// line containment tests. All the functionality supported by this
// class is implemented by the class AcBrImpHit.
//
// This class defines the functions that are pertinent to hit objects,
// and cannot be directly set by the user as the initialisation
// requirements are only available internally at the time of a call
// to AcBrEntity::getLineContainment(). It is derived from AcRxObject
// in order to provide full service run-time type-checking, etc.
//
// Hits are points generated by the intersection of a line with a
// solid (or subset of a solid), along with additional context. This
// class serves to contextualise all the hit data returned by line
// containment queries. A hit may correspond to one of the original
// end points of the line (if contained by the queried topology
// object), or it may also be a point on the geometric bounds at
// which a line is broken into segments; a transition between what
// is inside and what is outside the queried topology object.
//
// The AcRxObject::isEqualTo() equivalence function is redefined to
// check content equality between two hit objects. kTrue is returned
// if this object is valid and has been equated to another valid hit
// object. Equivalence is defined as having the same internal data.
//
// The isNull() validator function tests whether this hit object
// has been set to anything meaningful. kTrue is returned if it is
// uninitialised; kFalse is returned if it is valid/initialised.
//
// The setHitPath() hit data initialiser is deprecated in favour of set().
//
// The getPoint() model space point query is deprecated in favour of the
// efficient new getPoint() query which sets an already-instantiated point.
//
// The getEntityHit() hit topology query returns the dimensionally
// lowest topology object that contains this hit. Note that the start
// and end points of lines are classified as hits as long as they pass
// a point containment test against the object whose line containment
// test generated this hit object. It is not necessary for the line to
// pass through the geometric bounds; a hit or pair of hits may reside 
// in the interior of a solid. The topology object is passed as a null
// AcBrEntity base class reference pointer for getEntityHit() to
// instantiate. If this hit object is uninitialised, eUninitialisedObject
// is returned. If the AutoCAD object associated with the topology
// object whose line containment test generated this hit object has
// been modified since this hit object's internal data was last set,
// eBrepChanged is returned. If the AcBrEntity allocation comes back
// null, Acad::eOutOfMemory is returned. In the event of an error, the
// topology reference pointer is unchanged and thus likely points to
// a null object. 
//
// The getEntityEntered() entered topology query returns the dimensionally
// lowest topology object that contains the segment along the original
// line bound by this hit and the next hit, or a null pointer if this is
// either the final hit in the hit array or the segment exits and then
// re-enters the topology object whose line containment test was invoked.
// The topology object is passed as a null AcBrEntity base class reference
// pointer for getEntityEntered() to instantiate. If this hit object is
// uninitialised, eUninitialisedObject is returned. If the AutoCAD object
// associated with the topology object whose line containment test
// generated this hit object has been modified since this hit object's
// internal data was last set, eBrepChanged is returned. If the AcBrEntity
// allocation comes back null, Acad::eOutOfMemory is returned. In the
// event of an error, the topology reference pointer is unchanged and
// thus likely points to a null object. 
//
// The getPoint() model space point query returns this hit's underlying
// point as an AcGePoint3d, with the entire chain of transforms from the
// associated topology object's subentity path. The associated topology
// object is not currently stored, but is the object whose line
// containment test generated this hit object. The point is instantiated
// by the user and passed by reference pointer for getPoint() to set.
// If this hit object is uninitialised, eUninitialisedObject is returned.
// In the event of an error, the point reference argument's value is
// unchanged.
//
// The getEntityAssociated() associated topology query returns the topology
// object whose line containment test generated this hit object. The
// topology object is passed as a null AcBrEntity base class reference
// pointer for getEntityAssociated() to instantiate. If this hit object is
// uninitialised, eUninitialisedObject is returned. If the AutoCAD object
// associated with the topology object has been modified since this hit
// object's internal data was last set, eBrepChanged is returned. If the
// AcBrEntity allocation comes back null, Acad::eOutOfMemory is returned.
// If the associated topology object fails to map to a valid subentity ID,
// Acad::eNotInDatabase is returned. In the event of an error, the topology
// reference pointer is unchanged and thus likely points to a null object.
//
// The setValidationLevel() prioritisation function sets the validation
// level to be used in all data queries that require access to the
// associated AutoCAD object. In general, this means any function that
// accesses the brep topology. If set to kNoValidation, eBrepChanged
// will no longer be returned by functions called on this mesh object.
// Any query that returns a newly instantiated AcBr object uses this
// mesh object's validation level to initialise the new object.
//
// The getValidationLevel() prioritisation query returns a dedicated
// ValidationType enum corresponding to the validation level currrently
// being used by this hit object.
//
// The brepChanged() status query returns a simple Boolean indicating
// whether the associated AutoCAD object has changed since this hit
// object was last set. kFalse is returned if it has not changed or
// if the associated object is non-database resident; kTrue is returned
// either if it has changed or if it is not possible to determine
// whether it has changed (which generally indicates that the AutoCAD
// object has gone out of scope due to deletion).
//
// The set() hit data initialiser is for internal use only. It is used
// to set this hit object's internal data using an unexporyted type.
//
// The get() hit data query is for internal use only. It retrieves this
// hit object's internal data using an unexported type.


#include "adesk.h"
#include "rxobject.h"
#include "rxboiler.h"
#include "brgbl.h"


// forward class declarations
class AcGePoint3d;
class AcBrEntity;
class AcBrHitData;
class AcBrImpHit;


// this is a temporary typedef to guarantee binary compatibility
typedef AcBrHitData AcBrHitPath;


class AcBrHit : public AcRxObject
{
public:
    ACRX_DECLARE_MEMBERS(AcBrHit);
    AcBrHit();
    AcBrHit(const AcBrHit& src);
    ~AcBrHit();

    // Assignment operator
    AcBrHit&            operator =      (const AcBrHit& src);

    // Equivalence                    
    Adesk::Boolean      isEqualTo       (const AcRxObject* other) const;
    
    // Queries & Initialisers
    Adesk::Boolean      isNull          () const;
	// (Note: obsolete function)
    AcBr::ErrorStatus   setHitPath	    (AcBrHitPath& hitPath);

    // Geometry (Note: deprecated function)
    AcBr::ErrorStatus   getPoint        (AcGePoint3d*& point) const;

    // Topological Containment
    AcBr::ErrorStatus   getEntityHit    (AcBrEntity*& entityHit) const;
    AcBr::ErrorStatus   getEntityEntered(AcBrEntity*& entityEntered) const;

	// Topology
	AcBr::ErrorStatus   getEntityAssociated(AcBrEntity*& entity) const;

    // Geometry
    AcBr::ErrorStatus   getPoint        (AcGePoint3d& point) const;

	// Validation
	AcBr::ErrorStatus	setValidationLevel(const AcBr::ValidationLevel& validationLevel = *(AcBr::ValidationLevel*)NULL);
	AcBr::ErrorStatus	getValidationLevel(AcBr::ValidationLevel& validationLevel) const;
	Adesk::Boolean		brepChanged		() const;

    // Queries & Initialisers
    AcBr::ErrorStatus   set				(AcBrHitData* hitData);
    AcBr::ErrorStatus   get				(AcBrHitData*& hitData) const;

protected:
    AcBrImpHit*         mpImp;
};


#endif

