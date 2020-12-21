import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { DataComponent } from './components/tabla/data.component';
import { MaterialModule } from './material/material.module';
import { MatButtonModule } from '@angular/material/button';
import { EditorComponent } from './components/editor/editor.component';
import { FormsModule } from '@angular/forms';
import { CodemirrorModule } from '@ctrl/ngx-codemirror';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { ComponenteNavbarComponent } from './components/componente-navbar/componente-navbar.component';
import { TreeComponent } from './components/tree/tree.component';
import { HttpClientModule } from '@angular/common/http';


@NgModule({
  declarations: [
    AppComponent,
    DataComponent,
    EditorComponent,
    ComponenteNavbarComponent,
    TreeComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    MaterialModule,
    MatButtonModule,
    FormsModule,
    CodemirrorModule,
    FontAwesomeModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
