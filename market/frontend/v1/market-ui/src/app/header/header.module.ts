import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FlexLayoutModule } from "@angular/flex-layout";

import { FontAwesomeModule } from "@fortawesome/angular-fontawesome";

import { MaterialModule } from "../shared/material.module";
import { HeaderComponent } from './header.component';

@NgModule({
    imports: [
        CommonModule,
        FlexLayoutModule,
        FontAwesomeModule,
        MaterialModule
    ],
    declarations: [ HeaderComponent],
    exports: [ HeaderComponent ],
})
export class HeaderModule { }
